# Generated by Django 4.2.6 on 2023-10-19 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_remove_actor_sex_actor_gender_movie_running_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(),
        ),
    ]
