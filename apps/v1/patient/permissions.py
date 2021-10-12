from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk', None)
        if request.method == 'GET' and pk is not None:
            return request.user.is_operator or\
                request.user.is_patient
        elif request.method == 'GET':
            return request.user.is_admin or request.user.is_operator
        elif request.method == 'DELETE':
            return request.user.is_operator
        elif request.method == 'PATCH':
            return request.user.is_patient

        # If the request is using POST method
        return True