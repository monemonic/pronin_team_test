from django.db import models

from user_app.models import User
from utils_app.utils import image_file_path

from .constants import COLLECT_CONSTANTS
from .validators import check_date_end_collect


class CollectType(models.Model):
    """Модель вариантов подовов сбора"""
    name = models.CharField(
        verbose_name='Название',
        max_length=COLLECT_CONSTANTS['COLLECT_TYPE_NAME_MAX_LENGTH'],
    )

    class Meta:
        verbose_name = 'Повод сбора'
        verbose_name_plural = 'Поводы сбора'
        default_related_name = 'collect_types'

    def __str__(self):
        return self.name


class Collect(models.Model):
    """Модель создания группового сбора"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=COLLECT_CONSTANTS['COLLECT_NAME_MAX_LENGTH'],
    )
    collect_type = models.ForeignKey(
        CollectType,
        on_delete=models.CASCADE,
        verbose_name='Тип повода сбора',
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=COLLECT_CONSTANTS['COLLECT_DESCRIPTION_MAX_LENGTH'],
    )
    collect_target = models.PositiveBigIntegerField(
        verbose_name='Планируемая сумма сбора',
        null=True,
        blank=True,
        default=0
    )
    image = models.ImageField(
        verbose_name='Обложка сбора',
        upload_to=image_file_path,
        null=True,
        blank=True,
        default=None
    )
    collection_end_date = models.DateTimeField(
        verbose_name='Дата окончания сбора',
        validators=[check_date_end_collect]
    )

    class Meta:
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'
        default_related_name = 'collects'

    def __str__(self):
        """
        Переопределяем стандартный вывод метода __str__.

        Используется для более точного отображения данных об объекте курса.
        """
        return self.name[:30]


class Payment(models.Model):
    """Модель пожертвования для группового сбора"""
    donater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Жертвователь',
    )
    amount = models.PositiveBigIntegerField(
        verbose_name='Сумма пожертвования'
    )
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        verbose_name='Сбор',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания пожертвования'
    )

    class Meta:
        verbose_name = 'Пожертвование'
        verbose_name_plural = 'Пожертвования'
        default_related_name = 'payments'

    def __str__(self):
        """
        Переопределяем стандартный вывод метода __str__.

        Используется для более точного отображения данных об объекте курса.
        """
        return (
            f'Пожертвование {self.donater.get_full_name()[:30]} '
            f'сбору {self.collect.name}'
        )
