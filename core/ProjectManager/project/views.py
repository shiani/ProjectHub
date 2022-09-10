from user.serializers import UserSerialzier
from .serializers import AssignTaskSerializer, ProjectSerializer, TaskSerializer, AddProjectSerializer, \
    ProjectListOfTasksSerializer
from .permissions import ProjectManagerPermission
from django.db.transaction import atomic
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.http import Http404
from .models import Project, Task, AssignTask
from user.models import User


class AddProject(generics.CreateAPIView):
    serializer_class = AddProjectSerializer
    permission_classes = (ProjectManagerPermission, permissions.IsAuthenticated,)

    @atomic
    def post(self, request, *args, **kwargs):
        """Creates new Project"""
        context = {'request': request}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveProject(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (ProjectManagerPermission, permissions.IsAuthenticated)

    def get_object(self):
        try:
            return Project.objects.get(id=self.kwargs.get('project_id'), owner=self.request.user)
        except Project.DoesNotExist:
            raise Http404("Project not found")


class AddTask(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @atomic
    def post(self, request, *args, **kwargs):
        """Creates new Task"""
        title = request.data.get('title')
        description = request.data.get('description', None)
        project_id = request.data.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'message': "project not found"}, status=status.HTTP_400_BAD_REQUEST)
        task = Task.objects.create(title=title, description=description, project=project)
        serializer = TaskSerializer(instance=task)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssignTaskView(generics.CreateAPIView):  # developer and project manager
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
                    return Response({'message': "user position must be a developer to assign task"},
                                    status=status.HTTP_400_BAD_REQUEST)
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


class ListOfTaskInProject(generics.RetrieveAPIView):  # developer and project manager
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectListOfTasksSerializer

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'message': "project not found"}, status=status.HTTP_400_BAD_REQUEST)
        tasks = Task.objects.filter(project=project)
        serializer = ProjectListOfTasksSerializer(instance=project).data
        serializer["tasks"] = []
        for task in tasks:
            t = TaskSerializer(instance=task).data
            t['users'] = []
            assigned_tasks = AssignTask.objects.filter(task=task)
            for assigned_task in assigned_tasks:
                t['users'].append(UserSerialzier(instance=assigned_task.user).data)
            serializer["tasks"].append(t)

        return Response(serializer, status=status.HTTP_200_OK)


class ListOfUsersInProject(generics.RetrieveAPIView):  # project manager
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectListOfTasksSerializer

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'message': "project not found"}, status=status.HTTP_400_BAD_REQUEST)
        tasks = Task.objects.filter(project=project)

        serializer = ProjectSerializer(instance=project).data
        serializer["users"] = []
        for task in tasks:
            assigned_tasks = AssignTask.objects.filter(task=task)
            for assigned_task in assigned_tasks:
                user_data = UserSerialzier(instance=assigned_task.user).data
                if not user_data in serializer['users']:
                    serializer['users'].append(user_data)
        return Response(serializer, status=status.HTTP_200_OK)


class ListOfDeveloperTask(generics.RetrieveAPIView):  # developer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        assiend_tasks = AssignTask.objects.filter(user=self.request.user)
        data = {
            'username': request.user.email,
            'tasks': []
        }
        for assiend_task in assiend_tasks:
            tasks = Task.objects.filter(id=assiend_task.task.id)
            for task in tasks:
                data['tasks'].append(TaskSerializer(instance=task).data)

        return Response(data, status=status.HTTP_200_OK)


class ListOfAllProjects(generics.ListAPIView):  # project manager
    permission_classes = (ProjectManagerPermission, permissions.IsAuthenticated)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
