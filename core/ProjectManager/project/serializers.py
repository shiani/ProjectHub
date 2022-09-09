from rest_framework import serializers
from .models import Project, Task, AssignTask

class ProjejctSerializer(serializers.ModelSerializer):

    class Meta:
        model=Project
        fields = '__all__'

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

class AssignProjejctSerializer(serializers.ModelSerializer):

    class Meta:
        model=AssignTask
        fields = '__all__'