from rest_framework import serializers

from apps.v1.common.constants import BASE_EXCLUDE
from apps.v1.common.serializers import BaseSerializer
from .models import HealthRecord

class HealthRecordSerializer(BaseSerializer):
    class Meta:
        model = HealthRecord
        exclude = BASE_EXCLUDE
    