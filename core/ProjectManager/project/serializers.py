from rest_framework import serializers
from .models import Project, Task, AssignTask
from user.serializers import UserSignUpSerializer

class ProjejctSerializer(serializers.ModelSerializer):

    class Meta:
        model=Project
        fields = ['id', 'title', 'description']

class AddProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model=Project
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
        model=Task
        fields = '__all__'

class AssignTaskSerializer(serializers.ModelSerializer):
    # task = TaskSerializer()
    # user = UserSignUpSerializer()

    class Meta:
        model=AssignTask
        fields = ['task', 'user']

