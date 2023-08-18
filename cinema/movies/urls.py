from django.urls import path, include
from rest_framework import routers

from .views import HomeListView, MovieUpdateView, MovieDeleteView, \
    MovieDetailView, MovieListView, CreateMovieView
from .API.resource import Home, MovieViewSet


router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/create/', CreateMovieView.as_view(), name='movie_create'),
    path('movies/<int:pk>/update', MovieUpdateView.as_view(), name='movie_update'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    path('api/home/', Home.as_view(), name='home-rest'),
    path('api/', include(router.urls)),
]
