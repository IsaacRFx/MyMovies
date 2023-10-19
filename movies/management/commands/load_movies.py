import sys
from django.core.management.base import BaseCommand, CommandError
from movies.models import Actor, Genre, Movie, MovieCredit
import requests
import json
import os
from django.db import IntegrityError
from decouple import config



class Command(BaseCommand):
    help = "Load 20 random movies from TMDB API - discover/movie"
    

    def handle(self, *args, **options):
        api_base_url = config("TMDB_API_BASE_URL")
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + config("TMDB_READ_ACCESS_TOKEN"),
        }
        payload={
            "language": "es",
            "total_results": 20
        }
        response = requests.get(f"{api_base_url}/discover/movie", headers=headers, params=payload)
        print(response)
        movies = response.json()["results"]

        try:
            for movie in movies:
                try:
                    payload = {
                        "language": "es",
                        "append_to_response": "credits"
                    }
                    movie_request = requests.get(f"{api_base_url}/movie/{movie['id']}", headers=headers, params=payload)
                    movie_data = movie_request.json()
                    movie_item = Movie.objects.get_or_create(
                        tmdb_movie_id=movie_data["id"],
                        title=movie_data["title"],
                        overview=movie_data["overview"],
                        release_date=movie_data["release_date"],
                        budget=movie_data["budget"],
                        running_time=movie_data["runtime"],
                        revenue = movie_data["revenue"],
                        poster_path = movie_data["poster_path"],
                    )

                    for genre in movie_data["genres"]:
                        genre_item = Genre.objects.get(tmdb_genre_id=genre["id"])
                        movie_item[0].genres.add(genre_item)
                    
                    for cast in movie_data["credits"]["cast"][:20]:
                        actor_request = requests.get(f"{api_base_url}/person/{cast['id']}", headers=headers)
                        actor_data = actor_request.json()
                        actor_item = Actor.objects.get_or_create(
                            tmdb_actor_id=actor_data["id"],
                            name=actor_data["name"],
                            gender=actor_data["gender"],
                            biography=actor_data["biography"],
                            birthday=actor_data["birthday"],
                            place_of_birth=actor_data["place_of_birth"],
                            profile_path=actor_data["profile_path"],
                        )
                        print(actor_item, movie_item)

                        credit_item = MovieCredit.objects.get_or_create(
                            actor=actor_item[0],
                            movie=movie_item[0],
                            role=cast["character"]
                        )

                    movie_credits = movie_item[0].credits.all()
                    for credit in movie_credits.get_queryset():
                        print(f"Actor: {credit.actor} - Movie: {credit.movie}, Role: {credit.role}")
                    # print(f"Movie genres: {movie_item[0].genres.all()}")

                    print(f"Movie {movie['title']} created")

                except IntegrityError:
                    print(f"Movie {movie['title']} already exists")

            print(f"Total moviess in DB: {Movie.objects.count()}")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)