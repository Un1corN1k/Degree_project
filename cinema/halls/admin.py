from django.contrib import admin
from .models import MovieSession, CinemaHall, Ticket


@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ['hall']


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ['name', 'size']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', "created_at", "seat_number"]
