from rest_framework import serializers

from apps.v1.common.constants import BASE_EXCLUDE
from apps.v1.patient.models import Patient
from .models import MedicineType, Medicine

class MedicineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineType
        exclude = BASE_EXCLUDE

class MedicineSerializer(serializers.ModelSerializer):
    patient_id = serializers.EmailField(write_only=True)
    patient = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Medicine
        exclude = BASE_EXCLUDE

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
        
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Custom
        new_password = validated_data.pop("password", None)
        if new_password is not None:
            instance.set_password(new_password)

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
        
        instance.save()
        return instance