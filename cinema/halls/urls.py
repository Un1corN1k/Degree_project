from django.urls import path, include
from rest_framework import routers

from .API.resource import CinemaHallViewSet, MovieSessionViewSet, ReserveSeatAPIView, SeatReservedAPIView
from .views import SeatReservedView, ReserveSeatView, CinemaHallListView, CinemaHallCreateView, \
    MovieSessionListView, MovieSessionDetailView, CreateMovieSessionView

router = routers.SimpleRouter()
router.register(r'cinema-halls', CinemaHallViewSet)
router.register(r'movie-sessions', MovieSessionViewSet)


urlpatterns = [
    path('cinema_halls/', CinemaHallListView.as_view(), name='cinema-hall-list'),
    path('cinema_halls/create/', CinemaHallCreateView.as_view(), name='cinema-hall-create'),
    path('movie_sessions/', MovieSessionListView.as_view(), name='movie-session-list'),
    path('movie-sessions/create/', CreateMovieSessionView.as_view(), name='movie-session-create'),
    path('movie_session/<int:pk>/', MovieSessionDetailView.as_view(), name='movie-sessions-detail'),
    path('reserve-seat/<int:movie_session_id>/', ReserveSeatView.as_view(), name='reserve_seat'),
    path('seat-reserved/<int:movie_session_id>/', SeatReservedView.as_view(), name='seat_reserved'),
    path('api/', include(router.urls)),
    path('api/reserve_seat/<int:movie_session_id>/', ReserveSeatAPIView.as_view(), name='reserve-seat'),
    path('api/seat-reserved/<int:movie_session_id>/', SeatReservedAPIView.as_view(), name='seat-reserved'),
]


