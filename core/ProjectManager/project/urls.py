from django.urls import path
from .views import AddProject, RetrieveProject, AddTask, AssignTaskView, ListOfTaskInProject, ListOfUsersInProject, ListOfDeveloperTask, ListOfAllProjects
app_name = 'project-api'

urlpatterns = [
    path('add_project/', AddProject.as_view(), name='add-project'),
    path('project/<project_id>/', RetrieveProject.as_view(), name='retrieve-project'),
    path('add_task/', AddTask.as_view(), name='add-task'),
    path('assign_task/', AssignTaskView.as_view(), name='assign-task'),
    path('project_tasks/<project_id>/', ListOfTaskInProject.as_view(), name='project-tasks'),
    path('project_users/<project_id>/', ListOfUsersInProject.as_view(), name='project-users'),
    path('user_task/', ListOfDeveloperTask.as_view(), name='user-tasks'),
    path('list_of_projects/', ListOfAllProjects.as_view(), name='list-of-projects'),

]