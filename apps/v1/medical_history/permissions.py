from rest_framework import permissions

from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, *args, **kwargs):
        return request.user.patient is not None