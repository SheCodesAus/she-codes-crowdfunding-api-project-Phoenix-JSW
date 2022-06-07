# Generated by Django 4.0.2 on 2022-06-06 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0020_pledge_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalShelter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=200)),
                ('charity', models.BigIntegerField()),
                ('is_approved', models.BooleanField(default=False)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='animal_shelter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animalspecies', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='animals',
            name='animal_species',
        ),
        migrations.RemoveField(
            model_name='animals',
            name='status',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='project',
        ),
        migrations.RemoveField(
            model_name='foster',
            name='user',
        ),
        migrations.RemoveField(
            model_name='support',
            name='user',
        ),
        migrations.RemoveField(
            model_name='project',
            name='animals',
        ),
        migrations.RemoveField(
            model_name='project',
            name='category',
        ),
        migrations.RemoveField(
            model_name='project',
            name='end_date',
        ),
        migrations.DeleteModel(
            name='Adopt',
        ),
        migrations.DeleteModel(
            name='Animals',
        ),
        migrations.DeleteModel(
            name='AnimalSpecies',
        ),
        migrations.DeleteModel(
            name='AnimalStatusTag',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='Foster',
        ),
        migrations.DeleteModel(
            name='Support',
        ),
        migrations.AddField(
            model_name='animalshelter',
            name='species',
            field=models.ManyToManyField(related_name='animal_shelter', related_query_name='animal_shelter', to='projects.AnimalTag'),
        ),
        migrations.AddField(
            model_name='project',
            name='species',
            field=models.ManyToManyField(related_name='projects', related_query_name='project', to='projects.AnimalTag'),
        ),
    ]
