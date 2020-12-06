from rest_framework import viewsets, status
from rest_framework_api_key.permissions import HasAPIAccess
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import HealthInstitution
from .serializers import HealthInstitutionSerializer
from .permissions import AuthorityPermission

# Create your views here.
class HealthInstitutionViewSet(viewsets.ModelViewSet):
    serializer_class = HealthInstitutionSerializer
    queryset = HealthInstitution.objects.all()

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        HasAPIAccess,
        AuthorityPermission,
    ]

    def get_queryset(self):
        return self.queryset

    def destroy(self, request, pk, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
