from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIAccess

from apps.v1.common.tools import get_object_or_none
from apps.v1.myauth.models import User
from apps.v1.patient.models import Patient
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
        elif self.request.user.role == User.Role.OPERATOR:
            patients_in_cluster = Patient.objects.filter(
                health_institution=self.request.user.operator.health_institution,
            )
            return self.queryset.filter(patient__in=patients_in_cluster)
        raise APIException("User role must be patient or operator")

    def partial_update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)