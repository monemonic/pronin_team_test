import pytest
from rest_framework import status


@pytest.mark.django_db(transaction=True)
class Test01CollectType:
    URL_COLLECT_TYPE = '/api/collect_type/'

    def test_availability_registration_endpoint(self, client):
        """Проверка наличия эндпоинта списка всех поводов сбора"""
        response = client.post(self.URL_COLLECT_TYPE)
        assert response.status_code != status.HTTP_404_NOT_FOUND
