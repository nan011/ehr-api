from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIAccess

from apps.v1.myauth.models import User
from apps.v1.common.tools import get_object_or_none
from .models import HealthRecord
from .permissions import AuthorityPermission, RedeemPermission
from .serializers import HealthRecordSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([RedeemPermission])
def redeem(request, pk):
    record = get_object_or_none(HealthRecord, **{'pk': pk})
    if record is None:
        return Response(
            data = {'detail': 'Unknown ID'},
            status = status.HTTP_404_NOT_FOUND,
        )

    if record.patient is not None:
        return Response(
            data = {'detail': 'Record has been taken'},
            status = status.HTTP_403_FORBIDDEN,
        )

    record.patient = request.user
    record.save()

    return Response(status = status.HTTP_204_NO_CONTENT)

class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    queryset = HealthRecord.objects.exclude(patient=None)

    permission_classes = [
        HasAPIAccess,
        AuthorityPermission,
    ]

    def get_queryset(self):
        if self.request.user.role == User.Role.PATIENT:
            return self.queryset.filter(patient=self.request.user)
        else:
            return self.queryset.filter(patient__health_institution=self.request.user.health_institution)

    def partial_update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)