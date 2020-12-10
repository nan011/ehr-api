from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.v1.common.serializers import BaseSerializer
from .models import Account

class AccountSerializer(BaseSerializer):
    class Meta:
        model = Account
        exclude = ('created_at', 'updated_at')
        extra_kwargs = {
            'is_active': {
                'read_only': True
            },
            'role': {
                'read_only': True
            },
            'password': {
                'write_only': True
            },
        }

    def update(self, instance, validated_data):
        new_password = validated_data.pop("password", None)
        if new_password is not None:
            instance.set_password(new_password)

        return super(__class__, self).update(instance, validated_data)

    def to_representation(self, instance, *args, **kwargs):
        representation = {
            'role': {
                'code': instance.role,
                'label': instance.get_role_display(),
            },
        }

        return {
            **super().to_representation(instance, *args, **kwargs),
            **representation,
        }

class UserSerializer(BaseSerializer):
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    account = AccountSerializer(many = False, read_only = True)

    def create(self, validated_data):
        validated_data['account'] = {
            'name': validated_data.pop('name'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
        }
        return super(__class__, self).create(validated_data)

    def update(self, instance, validated_data):
        data = {
            'name': validated_data.pop('name', None),
            'email': validated_data.pop('email', None),
            'password': validated_data.pop('password', None),
        }
        data = {key: value for (key, value) in data.items() if value is not None}
        account_serializer = AccountSerializer(
            data = data,
            partial = True,
        )
        account_serializer.is_valid(raise_exception=True)
        validated_data['account'] = account_serializer.save()

        return super(__class__, self).update(instance, validated_data)

    def to_representation(self, instance, *args, **kwargs):
        reps = super(__class__, self).to_representation(instance, *args, **kwargs)
        reps['id'] = reps['account'].pop('id')
        return reps

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    role = serializers.IntegerField()

    def validate(self, attrs):
        role = attrs.get('role')
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password, role=role)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
