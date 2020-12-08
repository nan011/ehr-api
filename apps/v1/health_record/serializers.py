from rest_framework import serializers

from apps.v1.common.constants import BASE_EXCLUDE
from .models import HealthRecord

class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        exclude = BASE_EXCLUDE
    