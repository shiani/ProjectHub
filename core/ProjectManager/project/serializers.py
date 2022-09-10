from dataclasses import fields
from rest_framework import serializers
from .models import Project, Task, AssignTask
from user.serializers import UserSerialzier


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description']


class AddProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description']

    def save(self, **kwargs):
        user = self.context['request'].user
        title = self.validated_data['title']
        if self.validated_data.get('description', None):
            description = self.validated_data['description']
        else:
            description = None

        return super().save(owner=user, title=title, description=description)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project_id']


class AssignTaskSerializer(serializers.ModelSerializer):
    # task = TaskSerializer()
    # user = UserSignUpSerializer()

    class Meta:
        model = AssignTask
        fields = ['task', 'user']


class ProjectListOfTasksSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tasks']
