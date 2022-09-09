from django.urls import path
from .views import AddProject, RetrieveProject
app_name = 'project-api'

urlpatterns = [
    path('add_project/', AddProject.as_view(), name='add-project'),
    path('retrieve_project/<id>/', RetrieveProject.as_view(), name='retrieve-project'),

]