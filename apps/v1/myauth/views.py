from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status, parsers, renderers
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

from apps.v1.common.tools import get_object_or_none
from .models import Token
from .serializers import AuthTokenSerializer
from .errors import TokenUnauthorizedError

# Create your views here.
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
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
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
        except TokenError:
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