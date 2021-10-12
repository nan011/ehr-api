from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIAccess

from apps.v1.common.tools import get_object_or_none
from apps.v1.lung_sound_classification.models import LungSoundClassification
from apps.v1.myauth.models import Account
from apps.v1.patient.models import Patient
from .models import HealthRecord
from .permissions import AuthorityPermission
from .serializers import HealthRecordSerializer

# Create your views here.
class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    queryset = HealthRecord.objects.exclude(patient=None)

    permission_classes = [
        HasAPIAccess,
        AuthorityPermission,
    ]

    def get_queryset(self):
        if self.request.user.is_patient:
            return self.queryset.filter(patient=self.request.user.id)
        elif self.request.user.is_operator:
            patients_in_cluster = Patient.objects.filter(
                health_institution=self.request.user.operator.health_institution,
            )
            return self.queryset.filter(patient__in=patients_in_cluster)
        raise APIException("Account role must be patient or operator")

    def create(self, request, *args, **kwargs):
        request.data
        request._full_data._mutable = True
        request._full_data.update({'patient_id': request.user.id})
        request._full_data._mutable = False

        return super(__class__, self).create(self. request, *args, **kwargs)


    def partial_update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)