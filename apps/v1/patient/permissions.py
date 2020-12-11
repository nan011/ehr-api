from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk', None)
        if request.method == 'GET' and pk is not None:
            return request.user.role == Account.Role.OPERATOR or\
                request.user.role == Account.Role.PATIENT
        elif request.method == 'GET' or request.method == 'DELETE':
            return request.user.role == Account.Role.OPERATOR
        elif request.method == 'PATCH':
            return request.user.role == Account.Role.PATIENT

        # If the request is using POST method
        return True