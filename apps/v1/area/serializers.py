from rest_framework import serializers

from apps.v1.common.constants import BASE_EXCLUDE
from .models import Province, City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = BASE_EXCLUDE + ('province',)

class ProvinceSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many = True)

    class Meta:
        model = Province
        exclude = BASE_EXCLUDE

    