from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sign-up', views.sign_up, name="sign_up"),
    path('movie/<int:movie_id>', views.movie_detail, name="movie_detail"),
    path('movie/<int:movie_id>/review', views.movie_review, name="movie_review"),
    path('actor/<int:actor_id>', views.actor_detail, name="actor_detail"),
]