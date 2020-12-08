from rest_framework import permissions
from apps.v1.myauth.models import User

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.get_role_display())
        if request.method != 'POST':
            return request.user.role == User.Role.OPERATOR or\
                request.user.role == User.Role.ADMIN
        elif request.method == 'DELETE':
            return request.user.role == User.Role.ADMIN
        return True