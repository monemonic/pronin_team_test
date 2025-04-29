import pytest
from rest_framework import status

from .utils import invalid_user_data, invalid_user_data_password


@pytest.mark.django_db(transaction=True)
class Test00UserRegistration:
    URL_SIGNUP = '/api/users/'

    def test_availability_registration_endpoint(
        self,
        client
    ):
        """Проверка наличия эндпоинта регистрации"""
        response = client.post(self.URL_SIGNUP)
        assert response.status_code != status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        'data', invalid_user_data + invalid_user_data_password
    )
    def test_invalid_data_user_registration(
        self,
        data,
        django_user_model,
        client
    ):
        """Проверка регистрации с неверными данными."""
        users_count = django_user_model.objects.count()
        response = client.post(self.URL_SIGNUP, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert users_count == django_user_model.objects.count()

    def test_valid_data_user_registration(
        self,
        valid_data_user_for_registration,
        django_user_model,
        client,
    ):
        """Проверка регистрации пользователя с правильными данными."""
        response = client.post(
            self.URL_SIGNUP, data=valid_data_user_for_registration
        )
        assert response.status_code == status.HTTP_201_CREATED
        new_user = django_user_model.objects.filter(
            email=valid_data_user_for_registration['email']
        )
        assert new_user.exists()

    def test_save_data_user_registration(
        self,
        client,
        data_user_after_registration,
        valid_data_user_for_registration,
    ):
        """
        Проверка, что данные пользователя верно сохраняются при регистрации.
        """
        response = client.post(
            self.URL_SIGNUP, data=valid_data_user_for_registration
        )
        assert response.status_code == status.HTTP_201_CREATED
        for key, value in data_user_after_registration.items():
            assert response.data[key] == value
