from django.contrib import admin
from .models import MovieSession, CinemaHall, Ticket


@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ['hall', 'start_time', 'end_time', 'hall_reservation_to', 'start_date', 'end_date']


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ['name', 'size']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', "reservation_date", 'movie_session', 'seat']
