from rest_framework import permissions
from django.core.exceptions import ValidationError

from apps.v1.common.tools import get_object_or_none
from apps.v1.myauth.models import User

class ActivationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk')
        targeted_user = get_object_or_none(User, **{"pk": pk})
        if targeted_user is None:
            raise ValidationError("A targeted user is unknown")

        if request.user.role == User.Role.ADMIN and targeted_user.role == User.Role.OPERATOR or\
            request.user.role == User.Role.OPERATOR and targeted_user.role == User.Role.PATIENT:
            request.data['targeted_user'] = targeted_user
            return True
        
        # Doesn't meet the rules:
        # - Admin -> Operator
        # - Operator -> Patient
        return False