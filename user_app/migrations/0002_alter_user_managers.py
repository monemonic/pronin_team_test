# Generated by Django 5.2 on 2025-04-18 17:21

import user_app.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', user_app.managers.UserManager()),
            ],
        ),
    ]
