from django.contrib import admin
from .models import MovieSession, CinemaHall


@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ['hall']


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ['name', 'size']
