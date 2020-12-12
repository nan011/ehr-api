from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIAccess

from .serializers import LungSoundClassificationSerializer
from .models import LungSoundClassification
from .permissions import AuthorityPermission

# Create your views here.
class LungSoundClassificationViewSet(viewsets.ModelViewSet):
    queryset = LungSoundClassification.objects.all()
    serializer_class = LungSoundClassificationSerializer
    permission_classes = [
        AuthorityPermission,
    ]

    def get_queryset(self):
        return self.queryset

    def retrieve(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def retrieve(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def destroy(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)