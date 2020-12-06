from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework_api_key.permissions import HasAPIAccess
from rest_framework.response import Response

from apps.v1.common.tools import get_user_or_none
from apps.v1.myauth.models import User
from .serializers import OperatorSerializer
from .models import Operator
from .permissions import AuthorityPermission, DeletePermission

# Create your views here.
class OperatorViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r'(.+@.+|me)'
    serializer_class = OperatorSerializer
    queryset = Operator.objects.all()
    permission_classes = [
        HasAPIAccess,
        AuthorityPermission,
        DeletePermission,
    ]

    def get_queryset(self):
        return self.queryset

    def list(self, request):
        return super().list(request)

    def retrieve(self, request, pk, *args, **kwargs):
        if pk.lower() == 'me':
            user = get_user_or_none(request)
            if user.role != User.Role.OPERATOR:
                return Response(status = status.HTTP_404_NOT_FOUND, data = {'detail': 'You are not an operator'})

            user_id = user.pk
            self.kwargs['pk'] = user_id
        else:
            self.kwargs['pk'] = pk

        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return super().update(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None, *args, **kwargs):
        if pk.lower() == 'me':
            user = get_user_or_none(request)
            if user.role != User.Role.OPERATOR:
                return Response(status = status.HTTP_404_NOT_FOUND, data = {'detail': 'You are not an operator'})

            user_id = user.pk
            self.kwargs['pk'] = user_id
        else:
            self.kwargs['pk'] = pk
        
        print(self.kwargs['pk'])

        return super().partial_update(request, *args, **kwargs)
