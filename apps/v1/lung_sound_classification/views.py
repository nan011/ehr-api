from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIAccess
from rest_framework.decorators import api_view, permission_classes

from apps.v1.common.constants import BASE_ALL_EXCLUDE
from apps.v1.common.pagination import DefaultLimitOffsetPagination
from .serializers import LungSoundClassificationSerializer
from .models import LungSoundClassification
from .permissions import AuthorityPermission

# @api_view(['GET'])
# @permission_classes([AuthorityPermission])
# def untaken_classifications(request):
#     paginator = DefaultLimitOffsetPagination()
#     lst = LungSoundClassification.objects.filter(health_record = None).values()
#     lst = [{key: value for key,value in item.items() if key not in BASE_ALL_EXCLUDE} for item in lst]
#     result = paginator.paginate_queryset(lst, request)
#     return paginator.get_paginated_response(result)

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