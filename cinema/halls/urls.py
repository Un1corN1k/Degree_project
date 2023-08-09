from django.urls import path
from .views import seat_reserved, reserve_seat, CinemaHallListView, CinemaHallCreateView, \
    MovieSessionListView, MovieSessionDetailView, create_movie_session

urlpatterns = [
    path('cinema_halls/', CinemaHallListView.as_view(), name='cinema-hall-list'),
    path('cinema_halls/create/', CinemaHallCreateView.as_view(), name='cinema-hall-create'),
    path('movie_sessions/', MovieSessionListView.as_view(), name='movie-session-list'),
    path('movie-sessions/create/', create_movie_session, name='movie-session-create'),
    path('movie_session/<int:pk>/', MovieSessionDetailView.as_view(), name='movie-sessions-detail'),
    path('reserve-seat/<int:session_id>/', reserve_seat, name='reserve_seat'),
    path('seat-reserved/<int:session_id>/', seat_reserved, name='seat_reserved'),
]
