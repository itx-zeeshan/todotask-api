from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, ProjectSerializer, TaskSerializer, SubtaskSerializer
from .models import User, Project, Task, Subtask
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@api_view(['GET'])
def get_users(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return Response({'success': False, 'message': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    users = User.objects.filter(is_staff=False, is_superuser=False)
    serializer = UserSerializer(users, many=True)
    return Response({'success': True, 'message': 'Users fetched successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'success': False, 'message': 'Both email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            return Response({'success': False, 'message': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    return Response({'success': True, 'message': 'User logged in successfully!', 'data': {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        }}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'User created successfully!', 'data': serializer.data}, status = status.HTTP_201_CREATED)
    
    first_error_message = next(iter(serializer.errors.values()))[0]
    return Response({ 'success': False, 'message': first_error_message}, status = status.HTTP_400_BAD_REQUEST)


#Project Apis
@api_view(['GET'])
def get_projects(request):
    
    if request.user.is_superuser and request.user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(user=request.user)
    
    serializer = ProjectSerializer(projects, many=True)
    return Response({'success': True, 'message': 'Projects fetched successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_project(request):
    serializer = ProjectSerializer(data = request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data,  'message': 'Project created successfully!'}, status = status.HTTP_201_CREATED)
    
    first_error_message = next(iter(serializer.errors.values()))[0]
    return Response({ 'success': False, 'message': first_error_message}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_project(request):
    id = request.data.get('id')

    if not id:
        return Response({'success': False, 'message': 'Project ID is required in the request body!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        project = Project.objects.get(user=request.user, id=id)
    except Project.DoesNotExist:
        return Response({'success': False, 'message': 'Project not found!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data, 'message': 'Project updated successfully!'}, status=status.HTTP_200_OK)

    first_error_message = next(iter(serializer.errors.values()))[0]
    return Response({'success': False, 'message': first_error_message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_project(request, project_id):
    try:
        project = Project.objects.get(user=request.user, id=project_id)
        project.delete()
        return Response({'success': True, 'message': 'Project deleted successfully!'}, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({'success': False, 'message': 'Project not found!'}, status=status.HTTP_404_NOT_FOUND)


#Task Apis
@api_view(['GET'])
def get_tasks(request):

    if request.user.is_superuser and request.user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(project__user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response({'success': True, 'message': 'Tasks fetched successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data = request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data,  'message': 'Task created successfully!'}, status = status.HTTP_201_CREATED)
    
    first_error_message = next(iter(serializer.errors.values()))[0]
    return Response({ 'success': False, 'message': first_error_message}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_task(request):
    id = request.data.get('id')

    if not id:
        return Response({'success': False, 'message': 'Task ID is required in the request body!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        task = Task.objects.get(project__user=request.user, id=id)
    except Task.DoesNotExist:
        return Response({'success': False, 'message': 'Task not found!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data, 'message': 'Task updated successfully!'}, status=status.HTTP_200_OK)

    first_error_message = next(iter(serializer.errors.values()))[0]
    return Response({'success': False, 'message': first_error_message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(project__user=request.user, id=task_id)
        task.delete()
        return Response({'success': True, 'message': 'Task deleted successfully!'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'success': False, 'message': 'Task not found!'}, status=status.HTTP_404_NOT_FOUND)


#Sub Task Apis
@api_view(['GET'])
def get_subtasks(request):
    if request.user.is_superuser and request.user.is_staff:
        subtasks = Subtask.objects.all()
    else:
        subtasks = Subtask.objects.filter(task__project__user=request.user)
    serializer = SubtaskSerializer(subtasks, many=True)
    return Response({'success': True, 'message': 'Sub Tasks fetched successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_subtask(request):
    serializer = SubtaskSerializer(data = request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data, 'message': 'Subtask created successfully!'}, status = status.HTTP_201_CREATED)
    
    first_error_message = next(iter(serializer.errors.values()))[0]
    return Response({ 'success': False, 'message': first_error_message}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_subtask(request):
    id = request.data.get('id')

    if not id:
        return Response({'success': False, 'message': 'Subtask ID is required in the request body!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        subtask = Subtask.objects.get(task__project__user=request.user, id=id)
    except Subtask.DoesNotExist:
        return Response({'success': False, 'message': 'Subtask not found!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SubtaskSerializer(subtask, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data, 'message': 'Subtask updated successfully!'}, status=status.HTTP_200_OK)

    first_error_message = next(iter(serializer.errors.values()))[0]
    return Response({'success': False, 'message': first_error_message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_subtask(request, subtask_id):
    try:
        subtask = Subtask.objects.get(task__project__user=request.user, id=subtask_id)
        subtask.delete()
        return Response({'success': True, 'message': 'Subtask deleted successfully!'}, status=status.HTTP_200_OK)
    except Subtask.DoesNotExist:
        return Response({'success': False, 'message': 'Subtask not found!'}, status=status.HTTP_404_NOT_FOUND)
    
