# Generated by Django 4.2.6 on 2023-10-19 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='sex',
        ),
        migrations.AddField(
            model_name='actor',
            name='gender',
            field=models.PositiveSmallIntegerField(choices=[(0, 'No especificado'), (1, 'Mujer'), (2, 'Hombre'), (3, 'No binario')], default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='running_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='credits',
            field=models.ManyToManyField(related_name='credits', through='movies.MovieCredit', to='movies.actor'),
        ),
    ]
