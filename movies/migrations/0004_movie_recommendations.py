# Generated by Django 4.2.6 on 2023-10-22 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_movie_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='recommendations',
            field=models.ManyToManyField(blank=True, to='movies.movie'),
        ),
    ]
