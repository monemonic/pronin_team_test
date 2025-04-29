import pytest
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture(autouse=True)
def fast_password_hashers():
    """
    Ускоряет хеширование паролей в тестах, заменяя алгоритм на быстрый MD5.
    """
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher'
    ]


@pytest.fixture
def valid_data_user_for_registration():
    return {
        'first_name': 'Тест',
        'last_name': 'Первый',
        'patronymic': 'Важный',
        'email': 'test1@mail.ru',
        'password': '123456qQ_',
        'phone': '+7 999 999-99-99'
    }


@pytest.fixture
def data_user_after_registration():
    return {
        'first_name': 'Тест',
        'last_name': 'Первый',
        'patronymic': 'Важный',
        'email': 'test1@mail.ru',
        'phone': '+7 999 999-99-99'
    }


@pytest.fixture
def user(django_user_model, valid_data_user_for_registration):
    """
    Создает пользователя с хешированным паролем
    """
    user = django_user_model(**valid_data_user_for_registration)
    user.set_password(valid_data_user_for_registration['password'])
    user.save()
    return user


@pytest.fixture
def user_client(user):
    client = APIClient()
    token = AccessToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create(
        first_name='Тест',
        last_name='Второй',
        patronymic='Ненужный',
        email='test2@mail.ru',
        password='123456q',
        phone='+7 (999) 999-99-91'
    )


@pytest.fixture
def another_user_client(another_user):
    client = APIClient()
    token = AccessToken.for_user(another_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client
