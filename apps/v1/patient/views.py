from rest_framework import status
from rest_framework_api_key.permissions import HasAPIAccess
from rest_framework.response import Response

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
        role_type = 'patient'
        role_name = 'patient'

    def retrieve(self, request, pk, *args, **kwargs):
        if request.user.is_patient and pk != "me":
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        return super(__class__, self).retrieve(request, pk, *args, **kwargs)
