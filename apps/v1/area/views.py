# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework_api_key.permissions import HasAPIAccess

from apps.v1.area import serializers, models

# Create your views here.
class ProvinceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProvinceSerializer
    queryset = models.Province.objects.all()
    permission_classes = [
        HasAPIAccess,
    ]

    def get_queryset(self):
        return self.queryset

    def retrieve(self, request, pk, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)