from datetime import timedelta, datetime

from django.core.exceptions import ValidationError
from django.db import models
from movies.models import Movie
from accounts.models import CustomUser
from django.urls import reverse


class CinemaHall(models.Model):
    name = models.CharField(max_length=200)
    size = models.PositiveIntegerField()
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
    reserved_seats_set = models.ManyToManyField("Ticket", blank=True)

    def get_available_seats(self):
        total_seats = self.hall.size
        reserved_seats = self.ticket_set.count()
        available_seats = total_seats - reserved_seats
        return available_seats

    def reserve_seat(self, seat_numbers, user):
        available_seats = self.get_available_seats()
        tickets = []

        for seat_number in seat_numbers:
            if available_seats > 0 and not Ticket.objects.filter(session=self, seat_number=seat_number).exists():
                ticket_price = self.movie.price
                ticket = Ticket.objects.create(user=user, session=self, seat_number=seat_number, price=ticket_price)
                tickets.append(ticket)
                available_seats -= 1

        return tickets

    def get_absolute_url(self):
        return reverse('reserve_seat', args=[str(self.id)])

    def __str__(self):
        return f"{self.movie.title} - {self.start_date} - {self.start_time}"

    def save(self, *args, **kwargs):
        if not self.end_time:
            movie_duration = self.movie.duration
            end_datetime = datetime.combine(datetime.today(), self.start_time) + timedelta(minutes=movie_duration)
            self.end_time = end_datetime.time()

        super().save(*args, **kwargs)


class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.session.movie.title} - Seat {self.seat_number}"
