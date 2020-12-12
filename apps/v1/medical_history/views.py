from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIAccess

from .serializers import MedicalHistorySerializer
from .models import MedicalHistory
from .permissions import AuthorityPermission

# Create your views here.
class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [
        HasAPIAccess,
        AuthorityPermission,
    ]

    def get_queryset(self):
        return self.queryset

    def list(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        request.data
        request._full_data._mutable = True
        request._full_data.update({'patient_id': request.user.id})
        request._full_data._mutable = False
        return super(__class__, self).create(request, *args, **kwargs)
    
    def retrieve(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return super().update(request, *args, **kwargs)

        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def destroy(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)