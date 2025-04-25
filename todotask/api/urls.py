from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('login_user/', views.login_user, name='login_user'),
    path('create_user/', views.create_user, name='create_user'),

    #Project urls
    path('projects/', views.get_projects, name='get_projects'),
    path('create_project/', views.create_project, name='create_project'),
    path('update_project/', views.update_project, name='update_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    
    #task urls
    path('tasks/', views.get_tasks, name='get_tasks'),
    path('create_task/', views.create_task, name='create_task'),
    path('update_task/', views.update_task, name='update_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),

   #Subtask urls
    path('subtasks/', views.get_subtasks, name='get_subtasks'),
    path('create_subtask/', views.create_subtask, name='create_subtask'),
    path('update_subtask/', views.update_subtask, name='update_subtask'),
    path('delete_subtask/<int:subtask_id>/', views.delete_subtask, name='delete_subtask'),
]