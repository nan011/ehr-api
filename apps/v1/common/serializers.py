import sys
import re

from django.db import models
from rest_framework import serializers

from apps.v1.common.tools import camel_case

class BaseSerializer(serializers.ModelSerializer):
    sub_model_classes = []
    
    def __init__(self, *args, **kwargs):
        self.sub_model_classes_dict = {SubModel().__class__.__name__: SubModel for SubModel in self.sub_model_classes}
        super(__class__, self).__init__(*args, **kwargs) 

    def create(self, validated_data):
        ModelClass = self.Meta.model
        
        for field_name in list(validated_data.keys()):
            field = self.fields[field_name]
            if isinstance(field, serializers.UUIDField):
                groups = re.search(r'^([a-zA-Z]+(_[a-zA-Z]+)*)_id$', field_name)
                if groups is not None:
                    new_field_name = groups[1]
                    SubModelClass = self.sub_model_classes_dict.get(camel_case(new_field_name))
                    validated_data[new_field_name] = SubModelClass.objects.get(pk = validated_data.pop(field_name))
            elif isinstance(field, serializers.BaseSerializer):
                SerializerClass = field.__class__

                serializer_field = SerializerClass(data = validated_data.pop(field_name), many = False)
                serializer_field.is_valid(raise_exception = True)
                validated_data[field_name] = serializer_field.save()
        
        obj = self.Meta.model.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        for field_name in list(validated_data.keys()):
            field = self.fields[field_name]
            if isinstance(field, serializers.UUIDField):
                groups = re.search(r'^([a-zA-Z]+(_[a-zA-Z]+)*)_id$', field_name)
                if groups is not None:
                    new_field_name = groups[1]
                    SubModelClass = self.sub_model_classes_dict.get(camel_case(new_field_name))
                    setattr(instance, new_field_name, SubModelClass.objects.get(pk = validated_data.pop(field_name)))
            elif isinstance(field, serializers.BaseSerializer):
                SerializerClass = field.__class__

                instance_child_data = validated_data.pop(field_name, None)
                if instance_child_data == None:
                    continue

                serializer_field = SerializerClass(
                    getattr(instance, field_name),
                    data = instance_child_data,
                    many = False,
                    partial = True,
                )
                serializer_field.is_valid(raise_exception = True)
                serializer_field.save()
            else:
                setattr(instance, field_name, validated_data.get(field_name, getattr(instance, field_name)))
        instance.save()
        return instance