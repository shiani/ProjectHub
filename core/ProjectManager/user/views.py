from django.shortcuts import render
from .serializers import UserSignUpSerializer
from rest_framework import generics, status
from django.db.transaction import atomic
from rest_framework.response import Response
from .permissions import RegisterPermission




class SignUp(generics.CreateAPIView):

    serializer_class = UserSignUpSerializer
    permission_classes = (RegisterPermission,)

    @atomic
    def post(self, request, *args, **kwargs):
        """Creates new user"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    