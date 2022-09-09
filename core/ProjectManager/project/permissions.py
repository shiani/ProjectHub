from rest_framework.permissions import BasePermission


class AddProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.position == "project manager"
        else:
            return False
