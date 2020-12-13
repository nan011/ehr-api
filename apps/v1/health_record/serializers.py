from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from apps.v1.common.constants import BASE_EXCLUDE, BASE_ALL_EXCLUDE
from apps.v1.common.serializers import BaseSerializer
from apps.v1.patient.models import Patient
from apps.v1.lung_sound_classification.models import LungSoundClassification
from apps.v1.lung_sound_classification.constants import RESERVED_IDS
from .models import HealthRecord

class LungSoundClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LungSoundClassification
        exclude = BASE_ALL_EXCLUDE + ('reserved_id',)

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

class HealthRecordSerializer(BaseSerializer):
    sub_model_classes = [Patient]
    patient_id = serializers.UUIDField(write_only = True)

    reserved_id = serializers.IntegerField(write_only=True, validators=[
        MinValueValidator(RESERVED_IDS[0]),
        MaxValueValidator(RESERVED_IDS[-1]),
    ])
    lung_sound_classification = LungSoundClassificationSerializer(read_only=True)
    class Meta:
        model = HealthRecord
        exclude = BASE_EXCLUDE

        extra_kwargs = {
            'patient': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        classification = \
            LungSoundClassification.objects.get(
                reserved_id = validated_data.pop('reserved_id'),
            )
        instance = super(__class__, self).create(validated_data)
        print(instance)
        classification.health_record = instance
        classification.save()
        return instance
        
    