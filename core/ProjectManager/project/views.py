from .serializers import ProjejctSerializer, TaskSerializer, AssignProjejctSerializer, AddProjectSerializer
from .permissions import AddProjectPermission, RetrieveProjectPermission
from django.db.transaction import atomic
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.http import Http404
from .models import Project

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