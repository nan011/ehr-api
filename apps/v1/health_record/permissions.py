from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_operator or\
                request.user.is_patient
        
        if request.method == 'POST':
            return request.user.is_patient

        return True