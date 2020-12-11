import sys
import re

from rest_framework import serializers
from .models import HealthInstitution
from apps.v1.common.serializers import BaseSerializer
from apps.v1.common.tools import camel_case
from apps.v1.common.constants import BASE_EXCLUDE
from apps.v1.area.serializers import CitySerializer
from apps.v1.area.models import Province, City

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        exclude = BASE_EXCLUDE

class HealthInstitutionFirstLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInstitution
        exclude = BASE_EXCLUDE

class HealthInstitutionSerializer(BaseSerializer):
    sub_model_classes = [City]
    province = ProvinceSerializer(many = False, read_only = True)

    city_id = serializers.UUIDField(write_only = True)
    city = CitySerializer(many = False, read_only = True)

    class Meta:
        model = HealthInstitution
        exclude = BASE_EXCLUDE

    def to_representation(self, instance, *args, **kwargs):
        reps = {
            'province': instance.city.province.values(),
        }

        return {
            **reps,
            **super(__class__, self).to_representation(instance, *args, **kwargs)
        }