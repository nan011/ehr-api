from rest_framework import serializers

from apps.v1.common.constants import BASE_ALL_EXCLUDE
from apps.v1.common.serializers import BaseSerializer
from apps.v1.patient.models import Patient
from .models import LungSoundClassification

class LungSoundClassificationSerializer(BaseSerializer):
    class Meta:
        model = LungSoundClassification
        exclude = BASE_ALL_EXCLUDE
        extra_kwargs = {
            'reserved_id': {
                'read_only': True,
            },
            'health_record': {
                'read_only': True,
            }
        }

    def to_representation(self, instance, *args, **kwargs):
        reps = {
            'result': {
                'code': instance.result,
                'label': instance.get_result_display(),
            }
        }

        return {
            **super(__class__, self).to_representation(instance, *args, **kwargs),
            **reps,
        }