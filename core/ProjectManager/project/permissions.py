from rest_framework.permissions import BasePermission
from rest_framework import permissions


class AddProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.position == "project manager"
        else:
            return False

class AddTaskPermission(BasePermission):
        def has_permission(self, request, view):
            return request.user.is_authenticated