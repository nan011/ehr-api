from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return request.user.role == Account.Role.OPERATOR or\
                request.user.role == Account.Role.ADMIN
        elif request.method == 'DELETE':
            return request.user.role == Account.Role.ADMIN
        return True