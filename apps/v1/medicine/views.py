from django.shortcuts import render
from django.http import QueryDict
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIAccess

from .models import Medicine, MedicineType
from .permissions import AuthorityPermission
from .serializers import MedicineTypeSerializer, MedicineSerializer

# Create your views here.
class MedicineTypeViewSet(viewsets.ModelViewSet):
    serializer_class = MedicineTypeSerializer
    queryset = MedicineType.objects.all()

    permission_classes = [
        HasAPIAccess,
    ]

    def get_queryset(self):
        return self.queryset

    def retrieve(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
        

class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()

    permission_classes = [
        HasAPIAccess,
        AuthorityPermission,
    ]

    def get_queryset(self):
        return self.queryset

    def create(self, request, *args, **kwargs):
        request.data
        request._full_data._mutable = True
        request._full_data.update({'patient_id': request.user.id})
        request._full_data._mutable = False
        return super(__class__, self).create(request, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, *args, **kwargs):
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)