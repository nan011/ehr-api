import sys
import re

from rest_framework import serializers
from .models import HealthInstitution
from apps.v1.area.serializers import CitySerializer
from apps.v1.area.models import Province, City
from apps.v1.common.tools import convert_to_camel_case
from apps.v1.common.constants import BASE_OUTPUT_MORE_EXCLUDE

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        exclude = BASE_OUTPUT_MORE_EXCLUDE


class HealthInstitutionSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(many = False, read_only = True)

    city_id = serializers.UUIDField(write_only = True)
    city = CitySerializer(many = False, read_only = True)

    class Meta:
        model = HealthInstitution
        exclude = BASE_OUTPUT_MORE_EXCLUDE
         
    def create(self, validated_data):
        ModelClass = self.Meta.model
        
        for field_name in list(validated_data.keys()):
            field = self.fields[field_name]
            if isinstance(field, serializers.UUIDField):
                groups = re.search(r'^([a-zA-Z]+(_[a-zA-Z]+)*)_id$', field_name)
                if groups is not None:
                    new_field_name = groups[1]
                    SubModelClass = getattr(sys.modules[__name__], convert_to_camel_case(new_field_name))
                    validated_data[new_field_name] = SubModelClass.objects.get(pk = validated_data.pop(field_name))
            elif isinstance(field, serializers.BaseSerializer):
                SerializerClass = field.__class__

                serializer_field = SerializerClass(data = validated_data.pop(field_name), many = False)
                serializer_field.is_valid(raise_exception = True)
                validated_data[field_name] = serializer_field.save()

        # Custom
        validated_data['province'] = validated_data['city'].province

        object = ModelClass.objects.create(
            **validated_data,
        )

        return object

    def update(self, instance, validated_data):
        for field_name in list(validated_data.keys()):
            field = self.fields[field_name]
            if isinstance(field, serializers.UUIDField):
                groups = re.search(r'^([a-zA-Z]+(_[a-zA-Z]+)*)_id$', field_name)
                if groups is not None:
                    new_field_name = groups[1]
                    SubModelClass = getattr(sys.modules[__name__], convert_to_camel_case(new_field_name))
                    setattr(instance, field_name, SubModelClass.objects.get(pk = validated_data.pop(field_name)))
            elif isinstance(field, serializers.BaseSerializer):
                SerializerClass = field.__class__

                instance_child_data = validated_data.pop(field_name, None)
                if instance_child_data == None:
                    continue

                serializer_field = SerializerClass(
                    getattr(instance, field_name),
                    data = instance_child_data,
                    many = False,
                )
                serializer_field.is_valid(raise_exception = True)
                serializer_field.save()
            else:
                setattr(instance, field_name, validated_data.get(field_name, getattr(instance, field_name)))
        
        # Custom
        instance.province = instance.city.province
        
        instance.save()
        return instance