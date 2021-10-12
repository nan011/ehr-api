from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PATCH' or request.method == 'GET':
            return request.user.is_operator or\
                request.user.is_admin
        elif request.method == 'DELETE':
            return request.user.is_admin

        # POST request is available for everyone
        return True