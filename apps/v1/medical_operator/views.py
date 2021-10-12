from rest_framework_api_key.permissions import HasAPIAccess
from apps.v1.myauth.views import UserViewSet
from .serializers import OperatorSerializer
from .models import Operator
from .permissions import AuthorityPermission

# Create your views here.
class OperatorViewSet(UserViewSet):
    serializer_class = OperatorSerializer
    queryset = Operator.objects.all()
    permission_classes = [
        HasAPIAccess,
        AuthorityPermission,
    ]

    class Meta:
        role_type = 'operator'
        role_name = "operator"
