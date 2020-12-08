from rest_framework import permissions
from django.core.exceptions import ValidationError

from apps.v1.myauth.models import User

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.PATIENT