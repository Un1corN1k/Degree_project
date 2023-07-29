from django.urls import path
from . import views
from .views import HomeListView, MovieUpdateView, MovieDeleteView, create_movie

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movies/create/', create_movie, name='movie_create'),
    path('movies/<int:pk>/update', MovieUpdateView.as_view(), name='movie_update'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
]
