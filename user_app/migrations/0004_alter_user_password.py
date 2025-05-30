# Generated by Django 5.2 on 2025-04-19 11:39

import django.core.validators
import user_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=1024, validators=[django.core.validators.MinLengthValidator(8), user_app.validators.validate_password]),
        ),
    ]
