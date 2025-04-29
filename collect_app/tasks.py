from celery import shared_task
from django.core.mail import send_mail

from config import settings as settings_django


@shared_task
def send_email_notification(user_id, message):
    """
    Celery задача для отправления письма пользователю с уведомлением
    """
    from user_app.models import User
    user = User.objects.get(pk=user_id)
    to = [user.email]

    send_mail(
        subject='Новое уведомление на ProninTeamDonate',
        message='Вы получили это письмо, поскольку вам '
                'пришло уведомление о том, что:\n\n'
                f'{message}\n',
        from_email=settings_django.EMAIL_HOST_USER,
        recipient_list=to,
    )
