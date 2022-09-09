from .serializers import ProjejctSerializer, TaskSerializer, AssignProjejctSerializer, AddProjectSerializer
from .permissions import AddProjectPermission
from django.db.transaction import atomic
from rest_framework import generics, status, permissions
from rest_framework.response import Response


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

