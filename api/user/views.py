from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from user_app.models import User
from user_app.user_swagger import USER_SWAGGER

from .serializers import UserSerializer


@extend_schema(tags=['Пользователь'],)
class UsersViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Этот ViewSet предоставляет метод для создания пользователей
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    @USER_SWAGGER['user_create']
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
