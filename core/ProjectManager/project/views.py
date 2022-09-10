from genericpath import exists
from .serializers import AssignTaskSerializer, ProjejctSerializer, TaskSerializer, AddProjectSerializer
from .permissions import AddProjectPermission
from django.db.transaction import atomic
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.http import Http404
from .models import Project, Task, AssignTask
from user.models import User


class AddProject(generics.CreateAPIView):
    serializer_class = AddProjectSerializer
    permission_classes = (AddProjectPermission, permissions.IsAuthenticated,)

    @atomic
    def post(self, request, *args, **kwargs):
        """Creates new Project"""
        context = {'request': request} 

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveProject(generics.RetrieveAPIView):
    serializer_class = ProjejctSerializer
    permission_classes = (AddProjectPermission, permissions.IsAuthenticated)

    def get_object(self):
        try:
            return Project.objects.get(id=self.kwargs.get('id'), owner=self.request.user)
        except Project.DoesNotExist:
            raise Http404("Project not found")

class AddTask(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @atomic
    def post(self, request, *args, **kwargs):
        """Creates new Task"""
        context = {'request': request} 
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssignTaskView(generics.CreateAPIView): # developer and project manager
    serializer_class = AssignTaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @atomic
    def post(self, request, *args, **kwargs):
        """Creates new Task"""
        task_id = request.data.get('task')
        user_id = request.data.get('user', None)

        # logic for project managers
        if request.user.position == "project manager":
            # project managers must assin task to a developer so we check that
            if not user_id:
                return Response({'message': "Request must include user id"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(id=user_id)
                if user.position != 'developer':
                    return Response({'message': "user position must be a developer to assign task"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': "user not found"}, status=status.HTTP_400_BAD_REQUEST)

            # finding task and assigning that to user
            try:
                task = Task.objects.get(id=task_id)

                if AssignTask.objects.filter(user=user, task=task).exists():
                    return Response({'message': "user already assined to task"}, status=status.HTTP_400_BAD_REQUEST)

                assign_task = AssignTask.objects.create(user=user, task=task)
            except Task.DoesNotExist:
                return Response({'message': "task not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # logic for developers
        else:
            # developers only can assign task to themselves
            user = request.user
            
            # finding task and assigning that to requested user
            try:
                task = Task.objects.get(id=task_id)

                if AssignTask.objects.filter(user=user, task=task).exists():
                    return Response({'message': "user already assined to task"}, status=status.HTTP_400_BAD_REQUEST)
                assign_task = AssignTask.objects.create(user=user, task=task)
            except Task.DoesNotExist:
                return Response({'task': "Not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AssignTaskSerializer(instance=assign_task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListOfTaskInProject(generics.ListAPIView): # developer and project manager
    pass


class ListOfDeveloperTask(generics.ListAPIView): # developer
    pass


class ListOfAllProjects(generics.ListAPIView): # project manager
    pass