from rest_framework.permissions import BasePermission


class AddProjectPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.position == "project manager"
