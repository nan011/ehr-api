from rest_framework import permissions
from apps.v1.myauth.models import Account

class AuthorityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.role == Account.Role.OPERATOR or\
                request.user.role == Account.Role.PATIENT

        return True

class RedeemPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Account.Role.PATIENT