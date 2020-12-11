from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PATCH' or request.method == 'GET':
            return request.user.role == Account.Role.OPERATOR or\
                request.user.role == Account.Role.ADMIN
        elif request.method == 'DELETE':
            return request.user.role == Account.Role.ADMIN

        # POST request is available for everyone
        return True