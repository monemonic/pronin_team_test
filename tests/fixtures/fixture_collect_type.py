import pytest

from collect_app.models import CollectType


@pytest.fixture
def collect_type(db):
    return CollectType.objects.create(name='Тест')


@pytest.fixture
def another_collect_type(db):
    return CollectType.objects.create(name='Тест2')
