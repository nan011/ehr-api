from rest_framework import serializers

from apps.v1.common.constants import BASE_EXCLUDE
from apps.v1.common.serializers import BaseSerializer
from apps.v1.patient.models import Patient
from .models import MedicalHistory

class MedicalHistorySerializer(BaseSerializer):
    sub_model_classes = [Patient]

    patient_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = MedicalHistory
        exclude = BASE_EXCLUDE
        extra_kwargs = {
            'patient': {
                'read_only': True,
            }
        }

    def to_representation(self, instance, *args, **kwargs):
        reps = {
            'relationship': {
                'code': instance.relationship,
                'label': instance.get_relationship_display(),
            }
        }

        return {
            **super(__class__, self).to_representation(instance, *args, **kwargs),
            **reps,
        }