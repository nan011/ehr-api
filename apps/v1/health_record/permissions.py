from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.operator is not None or\
                request.user.patient is not None
        
        if request.method == 'POST':
            return request.user.patient is not None

        return True