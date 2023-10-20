from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre
import requests
import json
import os
from django.db import IntegrityError
from decouple import config



class Command(BaseCommand):
    help = "Load movie genres from TMDB API - genre/movie/list"
    

    def handle(self, *args, **options):
        api_base_url = config("TMDB_API_BASE_URL")
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + config("TMDB_READ_ACCESS_TOKEN"),
        }
        payload={
            "language": "es"
        }
        response = requests.get(f"{api_base_url}/genre/movie/list", headers=headers, params=payload)
        genres = response.json()["genres"]

        try:
            for genre in genres:
                try:
                    Genre.objects.create(
                        tmdb_genre_id=genre["id"],
                        name=genre["name"],
                    )
                except IntegrityError:
                    print(f"Genre {genre['name']} already exists")

            print(f"Total genres in DB: {Genre.objects.count()}")

        except Exception as e:
            raise CommandError("Error loading genres: " + str(e))