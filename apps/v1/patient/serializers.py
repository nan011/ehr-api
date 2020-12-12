import sys
import re

from rest_framework import serializers

from apps.v1.myauth.serializers import UserSerializer
from apps.v1.health_institution.models import HealthInstitution
from apps.v1.health_institution.serializers import HealthInstitutionFirstLayerSerializer
from apps.v1.medical_history.serializers import MedicalHistorySerializer
from apps.v1.common.constants import BASE_EXCLUDE
from apps.v1.common.tools import camel_case
from apps.v1.medicine.serializers import MedicineSerializer
from .models import Patient

class PatientSerializer(UserSerializer):
    sub_model_classes = [HealthInstitution]
    health_institution_id = serializers.UUIDField(write_only=True)
    health_institution = HealthInstitutionFirstLayerSerializer(many=False, read_only=True)
    medicines = MedicineSerializer(many=True, read_only=True)
    medical_histories = MedicalHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance, *args, **kwargs):
        representation = {
            'physical_activity': {
                'code': instance.physical_activity,
                'label': instance.get_physical_activity_display(),
            }
        }

        return {
            **super().to_representation(instance, *args, **kwargs),
            **representation,
        }
    