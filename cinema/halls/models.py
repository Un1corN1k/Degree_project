from django.core.validators import MinValueValidator
from django.db import models
from movies.models import Movie
from accounts.models import CustomUser


class CinemaHall(models.Model):
    name = models.CharField(max_length=200)
    size = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.name


class MovieSession(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    reserved_seats = models.PositiveIntegerField(default=0)
    hall_reservation_to = models.TimeField(blank=True, null=True)

    def get_available_seats(self):
        total_seats = self.hall.size
        reserved_seats = self.ticket_set.count()
        available_seats = total_seats - reserved_seats
        return available_seats

    def __str__(self):
        return f"{self.movie.title} - {self.hall} - {self.start_time} - {self.end_time}"


class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    seat = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    reservation_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    price = models.DecimalField(validators=[MinValueValidator(1)], max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.movie_session.movie.title} - Seat {self.seat}"
