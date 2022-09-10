from django.urls import path
from .views import AddProject, RetrieveProject, AddTask, AssignTaskView
app_name = 'project-api'

urlpatterns = [
    path('add_project/', AddProject.as_view(), name='add-project'),
    path('retrieve_project/<id>/', RetrieveProject.as_view(), name='retrieve-project'),
    path('add_task/', AddTask.as_view(), name='add-task'),
    path('assign_task/', AssignTaskView.as_view(), name='assign-task'),

]