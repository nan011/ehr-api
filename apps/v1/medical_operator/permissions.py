from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PATCH' or request.method == 'GET':
            return request.user.operator is not None or\
                request.user.admin is not None
        elif request.method == 'DELETE':
            return request.user.admin is not None

        # POST request is available for everyone
        return True