from django.shortcuts import render, redirect
from .forms import SignUpForm
from movies.models import Movie
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