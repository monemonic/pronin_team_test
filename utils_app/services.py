import base64
import hashlib

from django.core.files.base import ContentFile
from rest_framework import serializers


class BaseService:
    @staticmethod
    def generate_cache_key(key):
        """Генерирует хешированный ключ для кэша."""
        return hashlib.md5(key.strip().lower().encode()).hexdigest()


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
