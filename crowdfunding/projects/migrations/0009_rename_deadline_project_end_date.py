# Generated by Django 4.0.2 on 2022-04-10 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_support_foster_adopt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='deadline',
            new_name='end_date',
        ),
    ]