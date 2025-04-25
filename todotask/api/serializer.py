from rest_framework import serializers
from .models import User, Project, Task, Subtask

class UserSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'projects']
        extra_kwargs = {
            'email': {'validators': []},
            'username': {'validators': []},
            'password': {'write_only': True}
        }

    def get_projects(self, obj):
        projects = Project.objects.filter(user=obj)
        return ProjectSerializer(projects, many=True).data

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Username is required.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'tasks']

    def get_tasks(self, obj):
        tasks = Task.objects.filter(project=obj)
        return TaskSerializer(tasks, many=True).data
    
    def validate_project_name(self, value):
        if not value:
            raise serializers.ValidationError("Project name is required.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project(
            project_name=validated_data['project_name'],
            user=user
        )
        project.save()
        return project

class TaskSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField()  # Accept project_id as input
    subtask = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'project_id', 'title', 'description', 'due_date', 'completed', 'created_at', 'subtask']

    def get_subtask(self, obj):
        subtasks = Subtask.objects.filter(task=obj)
        return SubtaskSerializer(subtasks, many=True).data

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        project_id = validated_data['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError(f"Project with id {project_id} does not exist.")
        

         # Check if the logged-in user owns the project
        if request and project.user != request.user:
            raise serializers.ValidationError({'project_id': "You do not have permission to assign tasks to this project."})

        task = Task(
            title=validated_data['title'],
            description=validated_data['description'],
            due_date=validated_data['due_date'],
            completed=validated_data['completed'],
            project=project
        )
        task.save()
        return task
    
class SubtaskSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField()

    class Meta:
        model = Subtask
        fields = ['id', 'task_id', 'title', 'description', 'due_date', 'completed', 'created_at']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        task_id = validated_data['task_id']
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError(f"Task with id {task_id} does not exist.")
        
        # Check if the logged-in user owns the task
        if request and task.project.user != request.user:
            raise serializers.ValidationError({'task_id': "You do not have permission to assign subtasks to this task."})

        subtask = Subtask(
            title=validated_data['title'],
            description=validated_data['description'],
            due_date=validated_data['due_date'],
            completed=validated_data['completed'],
            task=task
        )
        subtask.save()
        return subtask
