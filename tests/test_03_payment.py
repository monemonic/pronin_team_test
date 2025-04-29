import pytest
from rest_framework import status

from collect_app.models import Payment

from .utils import invalid_amount, invalid_collect


@pytest.mark.django_db(transaction=True)
class Test02Payment:
    URL_CREATE = '/api/payment/'

    @pytest.mark.parametrize(
        'data', invalid_amount
    )
    def test_invalid_data_user_create_payment_with_invalid_amount(
        self,
        data,
        user_client,
        collect_id_for_args
    ):
        """Проверка создания пожертвования с неверным значением amount."""
        collect_count = Payment.objects.count()
        data['collect'] = collect_id_for_args
        response = user_client.post(self.URL_CREATE, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert collect_count == Payment.objects.count()

    @pytest.mark.parametrize(
        'data', invalid_collect
    )
    def test_invalid_data_user_create_payment_with_invalid_collect(
        self,
        data,
        user_client
    ):
        """Проверка создания пожертвования с неверным значением collect."""
        collect_count = Payment.objects.count()
        response = user_client.post(self.URL_CREATE, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert collect_count == Payment.objects.count()

    @pytest.mark.django_db(transaction=True)
    def test_anonymous_user_create_payment(self, collect_data, client):
        """
        Проверка POST-запроса на добавление
        пожертвования анонимным пользователем.
        """
        response = client.post(self.URL_CREATE, data=collect_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Payment.objects.count() == 0

    @pytest.mark.django_db(transaction=True)
    def test_create_payment_valid_data(self, payment_valid_data, user_client):
        """
        Проверка POST-запроса на добавление
        пожертвования авторизованным пользователем с валидными данными.
        """
        response = user_client.post(self.URL_CREATE, data=payment_valid_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Payment.objects.count() == 1
        new_payment = response.data
        assert new_payment['collect'] == payment_valid_data['collect']
        assert new_payment['amount'] == str(payment_valid_data['amount'])
