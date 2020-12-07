from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status, parsers, renderers
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from apps.v1.common.tools import get_object_or_none
from .models import Token
from .serializers import AuthTokenSerializer
from .errors import TokenUnauthorizedError
from .permissions import ActivationPermission

# Create your views here.
@api_view(['GET'])
@permission_classes([ActivationPermission])
def activate(request, *args, **kwargs):
    targeted_user = request.data['targeted_user']
    targeted_user.is_active = True
    targeted_user.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([ActivationPermission])
def deactivate(request, *args, **kwargs):
    targeted_user = request.data['targeted_user']
    targeted_user.is_active = False
    targeted_user.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


class AuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        try:
            if not serializer.is_valid():
                raise TokenUnauthorizedError()

            user = serializer.validated_data['user']
            token = get_object_or_none(Token, user=user)
            
            if token != None:
                token.delete()
                
            new_token = Token.objects.create(user=user)

            return Response({
                'token': new_token.key,
            }, status=status.HTTP_200_OK)
        except TokenUnauthorizedError:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        try:
            if not serializer.is_valid():
                raise TokenUnauthorizedError()
                
            user = serializer.validated_data['user']
            token = get_object_or_none(Token, user=user)

            if token != None:
                token.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)