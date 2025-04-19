from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from collect_app.constants import COLLECT_CONSTANTS
from utils_app.services import BaseService

from .models import Collect, CollectType, Payment
from .tasks import send_email_notification


@receiver(post_save, sender=Collect)
@receiver(post_delete, sender=Collect)
@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def clear_collect_list_cache(sender, instance, **kwargs):
    """Очистка кешей списка сбора при изменении связанных данных"""
    pattern = COLLECT_CONSTANTS['CACHE_COLLECTS_LIST'].format(params='*')
    cache.delete_pattern(pattern)


@receiver(post_save, sender=CollectType)
@receiver(post_delete, sender=CollectType)
def clear_collect_type_cache(sender, instance, **kwargs):
    """Очистка кешей типов сбора при изменении связанных данных"""
    pattern = COLLECT_CONSTANTS['CACHE_COLLECT_TYPE_LIST']
    cache.delete_pattern(pattern)


@receiver(post_save, sender=Collect)
@receiver(post_delete, sender=Collect)
@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def clear_collect_retrieve_cache(sender, instance, **kwargs):
    """Очистка кеша указанного сбора, при изменении связанных данных"""
    if isinstance(instance, Collect):
        collect_id = instance.id
    else:
        collect_id = instance.collect.id

    collect_id_key = BaseService.generate_cache_key(str(collect_id))
    pattern = COLLECT_CONSTANTS['CACHE_RETRIEVE_COLLECT'].format(
        collect_id=collect_id_key
    )
    cache.delete_pattern(pattern)


@receiver(post_save, sender=Payment)
@receiver(post_save, sender=Collect)
def send_email_create_new_collect(sender, created, instance, **kwargs):
    """
    Отправка уведомления при создании нового сбора или нового пожертвования
    """
    if created:
        if isinstance(instance, Collect):
            message = COLLECT_CONSTANTS[
                'SEND_EMAIL_WITH_CREATED_NEW_COLLECT'
            ].format(name=instance.name)
            user = instance.author
        else:
            message = COLLECT_CONSTANTS[
                'SEND_EMAIL_WITH_CREATED_NEW_DONATE'
            ].format(name=instance.collect.name, amount=instance.amount)
            user = instance.donater

        send_email_notification(user, message)
