from rest_framework import permissions
from django.core.exceptions import ValidationError

from apps.v1.common.tools import get_object_or_none
from apps.v1.myauth.models import Account

class ActivationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk')
        if request.user.is_admin:
            targeted_user = get_object_or_none(Account, pk = pk)
        elif request.user.is_operator:
            targeted_user = get_object_or_none(Account, pk = pk)

        if targeted_user is None:
            raise ValidationError("A targeted user is unknown")

        request.data['targeted_user'] = targeted_user

        return True