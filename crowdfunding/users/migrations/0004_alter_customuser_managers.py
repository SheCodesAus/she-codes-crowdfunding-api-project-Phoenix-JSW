# Generated by Django 4.0.2 on 2022-05-01 15:19

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_applicant_alter_customuser_is_staff'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]
