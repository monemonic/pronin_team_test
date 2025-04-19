from django.core.exceptions import ValidationError
from django.utils import timezone


def check_date_end_collect(date):
    """Проверяет, что дата окончания сбора не меньше текущей даты."""
    time_now = timezone.now()
    if date < time_now:
        raise ValidationError('Дата не может быть меньше текущей')
