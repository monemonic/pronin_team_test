import pytest
from pytest_lazy_fixtures import lf
from rest_framework import status

from collect_app.models import Collect

from .utils import invalid_collect_data


@pytest.mark.django_db(transaction=True)
class Test02Collect:
    URL_LIST_AND_CREATE = '/api/collect/'
    COLLECT_WITH_ID = '/api/collect/{id}/'

    @pytest.mark.django_db(transaction=True)
    def test_anonymous_user_create_collect(self, collect_data, client):
        """
        Проверка POST-запросов на добавление
        сбора анонимным пользователем.
        """
        response = client.post(self.URL_LIST_AND_CREATE, data=collect_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Collect.objects.count() == 0

    @pytest.mark.django_db(transaction=True)
    def test_user_can_create_collect(
        self,
        collect_data,
        user_client,
        user
    ):
        """
        Проверка POST-запроса на добавление
        сбора авторизованным пользователем.
        """
        response = user_client.post(
            self.URL_LIST_AND_CREATE, data=collect_data
        )

        new_collect = response.data

        assert new_collect['author'] == user.id
        assert new_collect['name'] == collect_data['name']
        assert new_collect['collect_type'] == collect_data['collect_type']
        assert new_collect['description'] == collect_data['description']
        assert (
            str(new_collect['collect_target'])
            == str(collect_data['collect_target'])
        )
        assert new_collect['collection_end_date'].startswith(
            collect_data['collection_end_date'][:10]
        )

    def test_author_can_delete_collect(
            self,
            collect_id_for_args,
            user_client
    ):
        """Проверка удаления сбора автором."""
        response = user_client.delete(
            self.COLLECT_WITH_ID.format(id=collect_id_for_args)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Collect.objects.count() == 0

    @pytest.mark.parametrize(
        'users, expected_status', (
            (lf('another_user_client'), status.HTTP_403_FORBIDDEN),
            (lf('client'), status.HTTP_401_UNAUTHORIZED)
        )
    )
    def test_another_user_cant_delete_collect_of_user(
        self,
        collect_id_for_args,
        users,
        expected_status
    ):
        """Проверка удаления сбора не автором."""
        response = users.delete(
            self.COLLECT_WITH_ID.format(id=collect_id_for_args)
        )
        assert response.status_code == expected_status
        assert Collect.objects.count() == 1

    def test_author_can_edit_collect(
        self,
        collect_id_for_args,
        user_client,
        edit_collect_data,
        collect,

    ):
        """Проверка изменения сбора автором."""
        response = user_client.patch(
            self.COLLECT_WITH_ID.format(id=collect_id_for_args),
            data=edit_collect_data
        )
        assert response.status_code == status.HTTP_200_OK
        collect.refresh_from_db()
        assert collect.name == edit_collect_data['name']
        assert collect.collect_type.id == edit_collect_data['collect_type']
        assert collect.description == edit_collect_data['description']
        assert str(collect.collect_target) == str(
            edit_collect_data['collect_target']
        )
        assert str(collect.collection_end_date).startswith(
            edit_collect_data['collection_end_date'][:10]
        )

    @pytest.mark.parametrize(
        'users, expected_status', (
            (lf('another_user_client'), status.HTTP_403_FORBIDDEN),
            (lf('client'), status.HTTP_401_UNAUTHORIZED)
        )
    )
    def test_user_cant_edit_collect_of_another_user(
        self,
        collect_id_for_args,
        users,
        expected_status,
        edit_collect_data,
        collect
    ):
        """Проверка изменения сбора не автором."""
        response = users.patch(
            self.COLLECT_WITH_ID.format(id=collect_id_for_args),
            data=edit_collect_data
        )
        assert response.status_code == expected_status
        collect.refresh_from_db()
        assert collect.name != edit_collect_data['name']
        assert collect.collect_type.id != edit_collect_data['collect_type']
        assert collect.description != edit_collect_data['description']
        assert str(collect.collect_target) != str(
            edit_collect_data['collect_target']
        )
        assert not str(collect.collection_end_date).startswith(
            edit_collect_data['collection_end_date'][:10]
        )

    @pytest.mark.parametrize(
        'data', invalid_collect_data
    )
    def test_invalid_data_user_create_collect(self, data, user_client):
        """Проверка создания сбора с неверными данными."""
        collect_count = Collect.objects.count()
        response = user_client.post(self.URL_LIST_AND_CREATE, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert collect_count == Collect.objects.count()

    @pytest.mark.parametrize(
        'data', invalid_collect_data
    )
    def test_invalid_data_user_update_collect(
        self,
        data,
        user_client,
        collect_id_for_args,
    ):
        """Проверка создания сбора с неверными данными."""
        collect_count = Collect.objects.count()
        response = user_client.patch(
            self.COLLECT_WITH_ID.format(id=collect_id_for_args),
            data=data
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert collect_count == Collect.objects.count()
