from django.shortcuts import render, redirect
from .forms import SignUpForm
from movies.models import Movie
from movies.models import Actor
from movies.models import MovieReview
from movies.models import MovieCredit
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

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
    credits = MovieCredit.objects.filter(movie__tmdb_movie_id = movie_id)
    reviews = MovieReview.objects.filter(movie__tmdb_movie_id=movie_id)
    return render(request, 'movies/movie_detail.html', context={'credits': credits, 'reviews': reviews})

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