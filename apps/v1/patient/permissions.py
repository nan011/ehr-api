from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk', None)
        if request.method == 'GET' and pk is not None:
            return request.user.operator is not None or\
                request.user.patient is not None
        elif request.method == 'GET' or request.method == 'DELETE':
            return request.user.operator is not None
        elif request.method == 'PATCH':
            return request.user.patient is not None

        # If the request is using POST method
        return True