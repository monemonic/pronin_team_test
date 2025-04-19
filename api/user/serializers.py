from django.core.validators import MaxLengthValidator, MinLengthValidator
from phonenumbers import PhoneNumberFormat, format_number
from rest_framework import serializers

from user_app.constants import USER_CONSTANTS
from user_app.models import User
from user_app.validators import validate_password
from utils_app.services import Base64ImageField


class ReadMiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'avatar')


class UserSerializer(ReadMiniUserSerializer):
    """
    Сериализатор для создания пользователя.
    Валидирует поля и хэширует пароль перед сохранением.
    """
    avatar = Base64ImageField(required=False)
    password = serializers.CharField(
        write_only=True, validators=[
            MinLengthValidator(USER_CONSTANTS['MIN_LENGTH_PASSWORD']),
            MaxLengthValidator(USER_CONSTANTS['MAX_LENGTH_PASSWORD']),
            validate_password
        ]
    )

    class Meta:
        fields = ReadMiniUserSerializer.Meta.fields + (
            'email', 'phone', 'password', 'avatar'
        )
        model = User

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.phone:
            data['phone'] = format_number(
                instance.phone, PhoneNumberFormat.INTERNATIONAL
            )
        return data
