# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



class Genre(models.Model):
    tmdb_genre_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Actor(models.Model):

    GENDER_CHOICES = (
        (0, "No especificado"),
        (1, "Mujer"),
        (2, "Hombre"),
        (3, "No binario")
    )

    tmdb_actor_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=128)
    gender = models.PositiveSmallIntegerField(default=0, choices=GENDER_CHOICES)
    biography = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=128, blank=True)
    profile_path = models.URLField(blank=True)


    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_movie_id = models.IntegerField(blank=True, unique=True)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateField()
    budget = models.IntegerField(blank=True)
    running_time = models.IntegerField(default=0)
    revenue = models.IntegerField(blank=True)
    poster_path = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Actor, through="MovieCredit", related_name="credits")

    def __str__(self):
        return self.title


class MovieCredit(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    def __str__(self):
        return self.actor.name + "->" + self.role


class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                          MaxValueValidator(100)])
    review = models.TextField(blank=True)