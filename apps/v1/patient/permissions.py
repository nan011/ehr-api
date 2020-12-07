from rest_framework import permissions
from apps.v1.myauth.models import User

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            print(request.user.get_role_display())
            print(request.user)
            return request.user.role == User.Role.OPERATOR or\
                request.user.role == User.Role.PATIENT
        elif request.method == 'PATCH':
            return request.user.role == User.Role.PATIENT
        elif request.method == 'GET' or request.method == 'DELETE':
            print(request)
            return request.user.role == User.Role.OPERATOR

        # If the request is using POST method
        return True