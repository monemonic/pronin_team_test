from user_app.constants import USER_CONSTANTS
from collect_app.constants import COLLECT_CONSTANTS

invalid_user_data = [
    (
        {
            'email': ('a' * USER_CONSTANTS['MAX_LENGTH_EMAIL']) + '@yamdb.fake',
            'first_name': 'Юзер',
            'last_name': 'Юзеров',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'User1',
            'last_name': 'Юзеров',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'Юзер',
            'last_name': 'Userov1',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'Юзер',
            'last_name': 'Юзеров',
            'patronymic': 'Userovich1',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'Юзер',
            'last_name': 'Юзеров',
            'patronymic': 'Юзерович',
            'phone': '8 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': ('a' * (USER_CONSTANTS['MAX_LENGTH_FIRST_NAME'])),
            'last_name': 'Юзеров',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'Юзер',
            'last_name': ('a' * (USER_CONSTANTS['MAX_LENGTH_LAST_NAME'])),
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'Юзер',
            'last_name': 'Юзеров',
            'patronymic': ('a' * (USER_CONSTANTS['MAX_LENGTH_PATRONYMIC'])),
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': '  ',
            'last_name': 'Юзеров',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'User',
            'last_name': '  ',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'User',
            'last_name': 'Юзеров',
            'patronymic': '  ',
            'phone': '+7 999 999-99-99',
            'password': 'test_user123'
        }
    ),
]

invalid_user_data_password = [
    (
        {
            'email': 'user@user.fake',
            'first_name': 'Юзер',
            'last_name': 'Юзеров',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': ('1' * (USER_CONSTANTS['MAX_LENGTH_PASSWORD'] + 1)),
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'Юзер',
            'last_name': 'Юзеров',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': ('q' * (USER_CONSTANTS['MIN_LENGTH_PASSWORD'])),
        }
    ),
    (
        {
            'email': 'user@user.fake',
            'first_name': 'Юзер',
            'last_name': 'Юзеров',
            'patronymic': 'Юзерович',
            'phone': '+7 999 999-99-99',
            'password': ('1' * (USER_CONSTANTS['MIN_LENGTH_PASSWORD'] - 1)),
        }
    ),
]

invalid_collect_data = [
    (
        {
            'name': 'A' * (COLLECT_CONSTANTS['COLLECT_NAME_MAX_LENGTH'] + 1),
            'description': 'Описание нормальной длины',
            'collect_target': 10000,
            'collection_end_date': '2026-04-29T15:00:31',
        }
    ),
    (
        {
            'name': 'Нормальное название',
            'description': 'B' * (
                COLLECT_CONSTANTS['COLLECT_DESCRIPTION_MAX_LENGTH'] + 1
            ),
            'collect_target': 10000,
            'collection_end_date': '2026-04-29T15:00:31',
        }
    ),
    (
        {
            'name': 'Нормальное название',
            'description': 'Описание нормальной длины',
            'collect_target': (
                COLLECT_CONSTANTS['MIN_COLLECT_TARGET_VALUE'] - 1
            ),
            'collection_end_date': '22026-04-29T15:00:31',
        }
    ),
    (
        {
            'name': 'Нормальное название',
            'description': 'Описание нормальной длины',
            'collect_target': 10000,
            'collection_end_date': '2020-04-29T15:00:31',
        }
    ),
    (
        {
            'name': '',
            'description': 'Описание нормальной длины',
            'collect_target': 10000,
            'collection_end_date': '2026-04-29T15:00:31',
        }
    ),
    (
        {
            'name': 'Нормальное название',
            'description': '',
            'collect_target': 10000,
            'collection_end_date': '2026-04-29T15:00:31',
        }
    ),
    (
        {
            'name': 'Нормальное название',
            'description': 'Описание нормальной длины',
            'collect_target': 10000,
            'collection_end_date': '',
        }
    ),
]

invalid_amount = [

    (
        {
            'amount': str(COLLECT_CONSTANTS['MIN_DONATE_VALUE'] - 1),
        }
    ),
    (
        {
            'amount': '',
        }
    ),
    (
        {
            'amount': 'not_a_number',
        }
    )
]

invalid_collect = [
    (
        {
            'collect': '',
            'amount': '1000',
        }
    ),
    (
        {
            'collect': 'invalid_id',
            'amount': '1000',
        }
    ),
    (
        {
            'amount': '1000',
        }
    ),
]
