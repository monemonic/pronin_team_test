from django.core.management import BaseCommand

from user_app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.com',
            first_name='Админ',
            last_name='Админ',
            patronymic='Админ',
            is_active=True,
            is_staff=True,
            is_superuser=True,
            phone='+79999999999'
        )
        user.set_password('admin')
        user.save()
