import pytest


@pytest.fixture
def payment_valid_data(collect_id_for_args):
    return {
        'collect': collect_id_for_args,
        'amount': 1000
    }
