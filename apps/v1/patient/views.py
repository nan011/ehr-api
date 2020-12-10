from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework_api_key.permissions import HasAPIAccess
from rest_framework.response import Response

from apps.v1.common.tools import get_user_or_none
from apps.v1.myauth.models import Account
from apps.v1.myauth.views import UserViewSet
from .serializers import PatientSerializer
from .models import Patient
from .permissions import AuthorityPermission

# Create your views here.
class PatientViewSet(UserViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [
        HasAPIAccess,
        AuthorityPermission,
    ]

    class Meta:
        role_type = Account.Role.PATIENT
        role_name = 'patient'