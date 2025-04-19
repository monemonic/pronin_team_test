import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .constants import USER_CONSTANTS

email_validator = RegexValidator(
    regex=(
        # Имя пользователя (латиница, цифры, спецсимволы)
        r"^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
        # Дополнительные части, разделенные точками
        r"(\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
        # Точка не в конце имени пользователя
        r"(?<!\.)"
        # Поддомены
        r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?"
        # TLD (всегда заканчивается буквами длиной 2+)
        r"(?:\.[a-zA-Z]{2,})+$"
    ),
    message='Введите правильный адрес электронной почты.'
)


def cyrillic_latin_validator(value):
    """
    Проверяет, что значение содержит только буквы куриллицы или латиницы,
    пробелы, дефис, апостроф.
    """
    # Удаляем пробелы в начале и в конце строки
    value = value.strip()

    # Проверяем, что строка соответствует требованиям
    pattern = r'^[А-Яа-яЁёA-Za-z\s\'-]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Разрешены только кириллица, '
            'латиница, пробелы, дефисы и апострофы.'
        )

    # Проверяем, что строка не начинается и не заканчивается дефисом
    if value.startswith('-') or value.endswith('-'):
        raise ValidationError('Не может начинаться или заканчиваться дефисом.')

    if value.startswith("'") or value.endswith("'"):
        raise ValidationError(
            'Не может начинаться или заканчиваться апострофом.'
        )


def optional_min_length_validator(value):
    """
    Проверяет минимальную длину, если значение не пустое.
    """
    min_length = USER_CONSTANTS['MIN_LENGTH_PATRONYMIC']
    if value and len(value) < min_length:
        raise ValidationError(
            f'Минимальная длина — {min_length} символов.'
        )
    return value


def validate_password(password):
    """
    Проверяет, что пароль соответствует следующим требованиям:
    - Допустима только латиница (верхний и нижний регистр),
        цифры и перечисленные специальные символы.
    - Обязательно должна быть хотя бы одна цифра.
    - Обязательно должен быть хотя бы один специальный символ.
    - Обязательно должна быть хотя бы одна заглавная буква.
    - Обязательно должна быть хотя бы одна строчная буква.
    - Пробелы недопустимы (внутри).
    """

    # Проверка на пробелы
    if ' ' in password:
        raise ValidationError('Пароль не должен содержать пробелы.')

    # Список допустимых специальных символов (без лишнего экранирования)
    allowed_special_characters = '!@#()$%*&\\_-+=}{;:,.<>/?^|~\'"'

    checks_patterns = {
        rf'^[A-Za-z0-9{re.escape(allowed_special_characters)}]+$': (
            'Пароль может содержать только '
            'латинские буквы, цифры и допустимые '
            f'специальные символы: {allowed_special_characters}.'
        ),
        r'[0-9]': 'Пароль должен содержать хотя бы одну цифру.',
        rf'[{re.escape(allowed_special_characters)}]': (
            f'Пароль должен содержать хотя бы один специальный символ '
            f'из списка: {allowed_special_characters}.'
        ),
        r'[A-Z]': 'Пароль должен содержать хотя бы одну заглавную букву.',
        r'[a-z]': 'Пароль должен содержать хотя бы одну строчную букву.'
    }

    for pattern, error_message in checks_patterns.items():
        if not re.search(pattern, password):
            raise ValidationError(error_message)

    return password
