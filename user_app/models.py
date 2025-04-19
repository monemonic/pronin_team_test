from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from utils_app.utils import image_file_path

from .constants import USER_CONSTANTS
from .managers import UserManager
from .validators import (cyrillic_latin_validator, email_validator,
                         optional_min_length_validator, validate_password)


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Использует email как уникальный идентификатор вместо username.
    """
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Почта',
        help_text='Электронная почта пользователя',
        validators=[
            email_validator,
            MinLengthValidator(USER_CONSTANTS['MIN_LENGTH_EMAIL'])
        ]
    )
    first_name = models.CharField(
        max_length=USER_CONSTANTS['MAX_LENGTH_FIRST_NAME'],
        verbose_name='Имя',
        help_text='Имя пользователя',
        validators=[
            cyrillic_latin_validator, MinLengthValidator(
                USER_CONSTANTS['MIN_LENGTH_FIRST_NAME']
            )
        ]
    )
    last_name = models.CharField(
        max_length=USER_CONSTANTS['MAX_LENGTH_LAST_NAME'],
        verbose_name='Фамилия',
        help_text='Фамилия пользователя',
        validators=[
            cyrillic_latin_validator, MinLengthValidator(
                USER_CONSTANTS['MIN_LENGTH_LAST_NAME']
            )
        ]
    )
    patronymic = models.CharField(
        max_length=USER_CONSTANTS['MAX_LENGTH_PATRONYMIC'],
        verbose_name='Отчество',
        help_text='Отчество пользователя',
        blank=True,
        validators=[cyrillic_latin_validator, optional_min_length_validator]
    )
    phone = PhoneNumberField(
        verbose_name='Номер телефона',
        unique=True,
        help_text='Номер телефона пользователя',
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to=image_file_path,
        null=True,
        blank=True,
        default=None
    )
    password = models.CharField(
        max_length=USER_CONSTANTS['MAX_LENGTH_PASSWORD'],
        validators=[
            MinLengthValidator(USER_CONSTANTS['MIN_LENGTH_PASSWORD']),
            validate_password
        ]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()
