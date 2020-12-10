from rest_framework import serializers

from apps.v1.common.serializers import BaseSerializer
from apps.v1.common.constants import BASE_EXCLUDE, BASE_ALL_EXCLUDE
from apps.v1.patient.models import Patient
from .models import MedicineType, Medicine

class MedicineTypeSerializer(BaseSerializer):
    class Meta:
        model = MedicineType
        exclude = BASE_EXCLUDE

class MedicineSerializer(BaseSerializer):
    sub_model_classes = [Patient]
    patient_id = serializers.UUIDField(write_only=True)
    patient = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Medicine
        exclude = BASE_ALL_EXCLUDE