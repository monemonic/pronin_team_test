from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

from api.mixins import CreateMixin
from user_app.models import User
from user_app.user_swagger import USER_SWAGGER

from .serializers import UserSerializer


@extend_schema(tags=['Пользователь'],)
class UsersViewSet(CreateMixin):
    """
    Этот ViewSet предоставляет метод для создания пользователей
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    @USER_SWAGGER['user_create']
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
