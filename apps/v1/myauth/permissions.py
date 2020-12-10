from rest_framework import permissions
from django.core.exceptions import ValidationError

from apps.v1.common.tools import get_object_or_none
from apps.v1.myauth.models import Account

class ActivationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk')
        if request.user.role == Account.Role.ADMIN:
            targeted_user = get_object_or_none(Account, pk = pk, role = Account.Role.OPERATOR)
        elif request.user.role == Account.Role.OPERATOR:
            targeted_user = get_object_or_none(Account, pk = pk, role = Account.Role.PATIENT)

        if targeted_user is None:
            raise ValidationError("A targeted user is unknown")

        request.data['targeted_user'] = targeted_user

        return True