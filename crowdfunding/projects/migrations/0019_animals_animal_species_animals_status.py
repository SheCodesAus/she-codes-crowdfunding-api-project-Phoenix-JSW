# Generated by Django 4.0.2 on 2022-05-07 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_remove_animals_animal_species_remove_animals_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='animals',
            name='animal_species',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='projects.animalspecies', verbose_name='Animal Species'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='animals',
            name='status',
            field=models.ManyToManyField(related_name='animals', related_query_name='animal', to='projects.AnimalStatusTag'),
        ),
    ]
