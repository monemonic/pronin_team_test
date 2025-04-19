from datetime import datetime
from random import choice, randint

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from collect_app.models import Collect, CollectType, Payment
from user_app.models import User


fake = Faker('ru_RU')

unique_emails = set()
unique_phones = set()


def generate_unique_email():
    """Метод создания уникального email адреса"""
    while True:
        email = fake.unique.email()
        if email not in unique_emails:
            unique_emails.add(email)
            return email


def generate_unique_phone():
    """Метод создания уникального номера телефона"""
    while True:
        phone = fake.unique.phone_number()
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 11 and digits.startswith('7'):
            phone = '+' + digits
        elif len(digits) == 10:
            phone = '+7' + digits
        else:
            continue
        if phone not in unique_phones:
            unique_phones.add(phone)
            return phone


class Command(BaseCommand):
    help = 'Генерирует моковые данные для тестов'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Количество данных для генерации
        num_users = 500
        num_collect_types = 20
        num_collects = 2000
        # Среднее количество пожертвований на сбор
        num_payments_per_collect = 5

        # Создание пользователей
        users = []
        for _ in range(num_users):
            users.append(User(
                email=generate_unique_email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                patronymic=fake.first_name_male(),
                phone=generate_unique_phone(),
                avatar=fake.image_url(),
                password='password123',
            ))
        User.objects.bulk_create(users)

        # Создаем типы подов сбора (CollectType)
        collect_types = []
        for _ in range(num_collect_types):
            collect_types.append(CollectType(
                name=fake.word()
            ))
        CollectType.objects.bulk_create(collect_types)

        # Создание промежутка для даты окончания сбора
        next_year = datetime.now().year + 1
        start_date = datetime(next_year, 1, 1)
        end_date = datetime(next_year, 12, 31)

        random_date = fake.date_between_dates(
            date_start=start_date, date_end=end_date
        )
        aware_end_date = timezone.make_aware(
            datetime.combine(random_date, datetime.min.time())
        )

        # Генерация сборов
        collects = []
        for _ in range(num_collects):
            collect = Collect(
                author=choice(users),
                name=fake.word(),
                collect_type=choice(collect_types),
                description=fake.text(),
                collect_target=randint(0, 10000),
                image=fake.image_url(),
                collection_end_date=aware_end_date,
            )
            collects.append(collect)

        Collect.objects.bulk_create(collects)

        # Создание промежутка для даты пожертвования
        last_year = datetime.now().year - 2
        start_date = datetime(last_year, 1, 1)
        end_date = datetime.now()

        # Генерация пожертвований
        payments = []
        for collect in collects:
            for _ in range(randint(1, num_payments_per_collect)):
                payments.append(Payment(
                    donater=choice(users),
                    amount=randint(100, 1000),
                    collect=collect,
                ))

        Payment.objects.bulk_create(payments)

        self.stdout.write(
            self.style.SUCCESS(
                f'Создано {num_users} пользователей, {num_collects} '
                'сборов и {len(payments)} пожертвований'
            )
        )
