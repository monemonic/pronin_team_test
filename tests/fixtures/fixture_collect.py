import pytest

from collect_app.models import Collect


@pytest.fixture
def collect_data(user, collect_type):
    return {
        'name': 'Описание',
        'collect_type': collect_type.id,
        'description': 'О сборе',
        "collect_target": 200,
        "collection_end_date": "2026-04-29T15:00:31"
    }


@pytest.fixture
def collect(user, collect_type):
    return Collect.objects.create(
        author=user,
        collect_type=collect_type,
        description='О сборе',
        collect_target=200,
        collection_end_date="2026-04-29T15:00:31"
    )


@pytest.fixture
def collect_id_for_args(collect):
    return collect.id


@pytest.fixture
def edit_collect_data(another_collect_type):
    return {
        'name': 'Описание 2',
        'description': 'О сборе 2',
        'collect_type': another_collect_type.id,
        "collect_target": 300,
        "collection_end_date": "2027-04-29T15:00:31"
    }
