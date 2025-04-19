import base64
import hashlib
import types
from functools import wraps

from django.core.cache import cache
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.response import Response


class BaseService:
    @staticmethod
    def generate_cache_key(key):
        """Генерирует хешированный ключ для кэша."""
        return hashlib.md5(key.strip().lower().encode()).hexdigest()

    @staticmethod
    def cache_response_decorator(generate_cache_key, timeout=600):
        """
        Декоратор для кеширования ответа с возможностью ручной генерации ключа.
        Подходит для методов, в которых не вызывается check_object_permissions

        :param generate_cache_key: Функция, которая генерирует ключ кеша, либо
            готовая переменная, которую можно использовать как ключ кеша
        :param timeout: Время жизни кеша в секундах.
        """
        def decorator(func):
            @wraps(func)
            def wrapped(self, request, *args, **kwargs):

                # Если передается метод, вызываем его
                if isinstance(generate_cache_key, types.FunctionType):
                    cache_key = generate_cache_key(
                        self, request, *args, **kwargs
                    )
                # Иначе используем переданный аргумент
                else:
                    cache_key = generate_cache_key

                cached_data = cache.get(cache_key)

                if cached_data is not None:
                    return Response(cached_data)

                # Если данных нет в кеше, вызываем оригинальный метод
                response = func(self, request, *args, **kwargs)

                # Сохраняем результат в кеш
                cache.set(cache_key, response.data, timeout)

                return response

            return wrapped
        return decorator


class Base64ImageField(serializers.ImageField):
    """Поле для обработки изображений, закодированных в формате Base64.

    Поле автоматически конвертирует строку в формате Base64 в
    файл изображения, который можно сохранить в базе данных.
    """

    def to_internal_value(self, data):
        """Преобразует данные из Base64 в файл изображения.

        Args:
            data (str): Строка изображения в формате Base64 или обычные данные.

        Returns:
            File: Объект файла, готовый для сохранения в модели.
        """
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
