import json
import os
import sys
from django.db import IntegrityError
from django.shortcuts import render, redirect
import requests
from .forms import SignUpForm
from movies.models import Genre, Movie
from movies.models import Actor
from movies.models import MovieReview
from movies.models import MovieCredit
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from decouple import config

# Create your views here.

def fetch_recommended_movies(movie_obj: Movie):
    api_base_url = config("TMDB_API_BASE_URL")
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + config("TMDB_READ_ACCESS_TOKEN"),
    }
    payload={
        "language": "es",
        "total_results": 5
    }
    response = requests.get(f"{api_base_url}/movie/{movie_obj.tmdb_movie_id}/recommendations", headers=headers, params=payload)
    movies = json.loads(response)
    return movies
    

def fetch_selected_movie(movie_obj: Movie):
    try:
        api_base_url = config("TMDB_API_BASE_URL")
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + config("TMDB_READ_ACCESS_TOKEN"),
        }
        payload={
            "language": "es",
            "append_to_response": "credits"
        }

        movie_request = requests.get(f"{api_base_url}/movie/{movie_obj.tmdb_movie_id}", headers=headers, params=payload)
        movie_data = movie_request.json()

        movie_item = Movie.objects.get_or_create(
            tmdb_movie_id=movie_data["id"],
            title=movie_data["title"],
            overview=movie_data["overview"],
            release_date=movie_data["release_date"] if movie_data["release_date"] != "" else None,
            budget=movie_data["budget"],
            running_time=movie_data["runtime"],
            revenue = movie_data["revenue"],
            poster_path = movie_data["poster_path"],
        )
        print(f"Created {movie_data['title']}")
        if movie_item[1] is True: # If movie was created
            for genre in movie_data["genres"]:
                genre_item = Genre.objects.get(tmdb_genre_id=genre["id"])
                movie_item[0].genres.add(genre_item)

        for cast in movie_data["credits"]["cast"][:10]:
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

            credit_item = MovieCredit.objects.get_or_create(
                actor=actor_item[0],
                movie=movie_obj,
                role=cast["character"]
            )
            print(f"Actor {actor_item[0]} added to {movie_obj} recommendations")

    except Exception as e:
        print(e)

def get_movie_recommended(movie_id: int):
    movie = Movie.objects.get(tmdb_movie_id=movie_id)
    return fetch_recommended_movies(movie)

def get_movie_credits(movie_id: int):
    movie = Movie.objects.get(tmdb_movie_id=movie_id)

    if not movie.credits.all():
        fetch_selected_movie(movie)

    credits = MovieCredit.objects.filter(movie=movie)

    return credits


def home(request):
    movies = Movie.objects.all()
    return render(request, 'movies/home.html', context={'movies': movies})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() # Save user
            login(request, user)
            return redirect('/home')
    else:
        form = SignUpForm()

    return render(request, 'registration/sign_up.html', context={'form': form})

def movie_detail(request, movie_id):
    # credits = get_movie_credits(movie_id)
    request.GET.get('fh')
    
    credits = get_movie_credits(movie_id)
    recommended = get_movie_recommended(movie_id)
    reviews = MovieReview.objects.filter(movie__tmdb_movie_id=movie_id)
    return render(request, 'movies/movie_detail.html', context={'credits': credits, 'recommended': recommended, 'reviews': reviews})

def movie_review(request, movie_id):
    if request.method == 'POST':
        review = MovieReview()
        review.user = request.user
        review.movie = Movie.objects.get(tmdb_movie_id=movie_id)
        review.review = request.POST['review']
        review.rating = request.POST['rating']
        review.save()
        return redirect('movie_detail', movie_id=movie_id)
    else:
        return render(request, 'movies/review.html', context={'movie_id': movie_id})

def actor_detail(request, actor_id):
    actor = Actor.objects.get(tmdb_actor_id=actor_id)
    return render(request, 'movies/actor_detail.html', context={'actor': actor})

