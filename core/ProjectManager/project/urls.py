from django.urls import path
from .views import AddProject
app_name = 'project-api'

urlpatterns = [
    path('add_project/', AddProject.as_view(), name='add-project'),
]