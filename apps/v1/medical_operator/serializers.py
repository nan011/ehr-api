from rest_framework import serializers

from apps.v1.myauth.serializers import UserSerializer
from apps.v1.health_institution.models import HealthInstitution
from apps.v1.health_institution.serializers import HealthInstitutionFirstLayerSerializer
from apps.v1.common.constants import BASE_EXCLUDE
from .models import Operator

class OperatorSerializer(UserSerializer):
    sub_model_classes = [HealthInstitution]
    health_institution_id = serializers.UUIDField(write_only=True)
    health_institution = HealthInstitutionFirstLayerSerializer(many=False, read_only=True)

    def create(self, validated_data):
        validated_data['is_active'] = False
        return super(__class__, self).create(validated_data)
    
    class Meta:
        model = Operator
        fields = '__all__'
        depth = 2
    