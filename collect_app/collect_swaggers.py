from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)

from api.collect.serializers import (CollectSerializer, CollectTypeSerializer,
                                     PaymentSerializer, ReadCollectSerializer)

NOT_AUTH_USER = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description='Неаутентифицированный пользователь',
    examples=[
        OpenApiExample(
            'Анонимный пользователь',
            value={'detail': 'Учетные данные не были предоставлены.'}
        ),
    ]
)

USER_NOT_AUTHOR = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description='Пользователь не является автором',
    examples=[
        OpenApiExample(
            'Запрос не от автора',
            value={
                'detail': (
                    'У вас недостаточно прав для '
                    'выполнения данного действия.'
                )
            }
        ),
    ]
)

OBJECT_NOT_FOUND = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description='Объект не найден',
    examples=[
        OpenApiExample(
            'Объект не найден',
            value={'detail': 'No Example matches the given query.'}
        ),
    ]
)

COLLETCT_TYPE_SWAGGER = {
    'list': extend_schema(
        summary='Список всех поводов сбора',
        description='Список всех доступных поводов сбора.',
        responses={
            200: CollectTypeSerializer
        }
    )
}

BASE_COLLECT_VALIDATE_ERROR = [
    OpenApiExample(
        'В поле collect_type несуществующий первичный ключ',
        value={'collect_type': [
            (
                'Недопустимый первичный ключ \"4\" '
                '- объект не существует.'
            )
        ]}
    ),
    OpenApiExample(
        'В поле collection_end_date дата меньше текущей',
        value={'collection_end_date': [
            (
                'Дата не может быть меньше текущей'
            )
        ]}
    ),
    OpenApiExample(
        'В collect_target передается не число',
        value={'collect_target': ['Требуется численное значение.']}
    ),
    OpenApiExample(
        'В collect_target передается число меньше 1',
        value={'collect_target': ['Убедитесь, что это значение больше либо равно 1.']}
    ),
]

COLLECT_SWAGGER = {
    'create': extend_schema(
        summary='Создание нового сбора',
        description=(
            'Создание нового сбора. Доступно '
            'только для авторизованного пользователя'
        ),
        responses={
            201: CollectSerializer,
            401: NOT_AUTH_USER,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description='Ошибка валидации данных',
                examples=BASE_COLLECT_VALIDATE_ERROR + [
                    OpenApiExample(
                        'Не указано поле одно из обязательных полей',
                        value={'example': ['Обязательное поле.']}
                    ),
                    OpenApiExample(
                        'Одно из обязательных полей пустое',
                        value={'example': ['Это поле не может быть пустым.']}
                    ),
                ]
            ),
        }
    ),
    'partial_update': extend_schema(
        summary='Редактирование существующего сбора',
        description=(
            'Редактирование существующего сбора. Доступно '
            'только для авторизованного пользователя являющегося автором сбора'
        ),
        responses={
            201: CollectSerializer,
            401: NOT_AUTH_USER,
            403: USER_NOT_AUTHOR,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description='Ошибка валидации данных',
                examples=BASE_COLLECT_VALIDATE_ERROR
            ),
            404: OBJECT_NOT_FOUND
        }
    ),
    'destroy': extend_schema(
        summary='Удаление сбора',
        description=(
            'Удаление существующего сбора. Доступно '
            'только для авторизованного пользователя являющегося автором сбора'
        ),
        responses={
            204: OpenApiResponse(description='Успешное удаление'),
            401: NOT_AUTH_USER,
            403: USER_NOT_AUTHOR,
            404: OBJECT_NOT_FOUND
        }
    ),
    'list': extend_schema(
        summary='Список всех сборов',
        description='Список всех доступных сборов.',
        responses={
            200: ReadCollectSerializer
        }
    ),
    'retrieve': extend_schema(
        summary='Сбор с указанным ID',
        description='Получение сбора с указанным в url ID.',
        responses={
            200: ReadCollectSerializer,
            404: OBJECT_NOT_FOUND
        }
    )
}


PAYMENT_SWAGGER = {
    'create': extend_schema(
        summary='Создание нового пожертвования',
        description=(
            'Создание нового пожертвования. Доступно '
            'только для авторизованного пользователя'
        ),
        responses={
            201: PaymentSerializer,
            401: NOT_AUTH_USER,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description='Ошибка валидации данных',
                examples=[
                    OpenApiExample(
                        'Не указано поле amount',
                        value={'amount': ['Обязательное поле.']}
                    ),
                    OpenApiExample(
                        'В поле amount указано невалидное значение',
                        value={'amount': ['Введите правильное число.']}
                    ),
                    OpenApiExample(
                        'Не указано поле collect',
                        value={'collect': ['Обязательное поле.']}
                    ),
                    OpenApiExample(
                        'В поле collect указано невалидное значение',
                        value={'collect': ['Некорректный тип. Ожидалось значение первичного ключа, получен str.']}
                    ),
                    OpenApiExample(
                        'В поле collect указано значение несуществующего сбора',
                        value={'collect': ['Недопустимый первичный ключ \"500000\" - объект не существует.']}
                    ),
                ]
            ),
        }
    ),
}
