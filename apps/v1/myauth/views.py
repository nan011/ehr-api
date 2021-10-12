from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status, parsers, renderers, viewsets
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from apps.v1.common.tools import get_object_or_none, get_user_or_none
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
            user.last_login = timezone.now()
            user.save()

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
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r'(.+)'

    def get_queryset(self):
        return self.queryset

    def __return_404_response(self):
        return Response(
            status = status.HTTP_404_NOT_FOUND,
            data = {'detail': 'Can\'t find you as {}'.format(self.Meta.role_name.lower())},
        )

    def __get_user_pk(self, request, pk):
        if pk.lower() == 'me':
            user = get_user_or_none(request)
            if getattr(user, self.Meta.role_type) is not None:
                return None
            user_id = user.pk
            pk = user_id
        return pk

    def retrieve(self, request, pk, *args, **kwargs):
        pk = self.__get_user_pk(request, pk)
        if pk is None:
            return self.__return_404_response()
        self.kwargs['pk'] = pk
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return super().update(request, *args, **kwargs)

        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None, *args, **kwargs):
        pk = self.__get_user_pk(request, pk)
        if pk is None:
            return self.__return_404_response()
        self.kwargs['pk'] = pk

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        pk = self.__get_user_pk(request, pk)
        if pk is None:
            return self.__return_404_response()
        self.kwargs['pk'] = pk

        return super().destroy(request, *args, **kwargs)