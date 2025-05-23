# Generated by Django 5.2 on 2025-04-29 13:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect_app', '0004_alter_collect_collect_target_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='collect_target',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Планируемая сумма сбора'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=20, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Сумма пожертвования'),
        ),
    ]
