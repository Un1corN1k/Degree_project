from django.urls import path
from . import views
from .views import CinemaHallListView, CinemaHallCreateView, MovieSessionListView, MovieSessionDetailView, reserve_seat

urlpatterns = [
    path('cinema_halls/', CinemaHallListView.as_view(), name='cinema-hall-list'),
    path('cinema_halls/create/', CinemaHallCreateView.as_view(), name='cinema-hall-create'),
    path('movie_sessions/', MovieSessionListView.as_view(), name='movie-session-list'),
    path('movie-sessions/create/', views.create_movie_session, name='movie-session-create'),
    path('movie_session/<int:pk>/', MovieSessionDetailView.as_view(), name='movie-sessions-detail'),
    path('movie-sessions/', views.movie_session_list, name='movie-session-list'),
    path('reserve-seat/<int:session_id>/', views.reserve_seat, name='reserve_seat'),
    path('seat-reserved/<int:session_id>/', views.seat_reserved, name='seat_reserved'),
]

