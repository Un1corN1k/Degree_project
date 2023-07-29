from django.db import models
from movies.models import Movie
from accounts.models import CustomUser


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
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    reserved_seats = models.PositiveIntegerField(default=0)
    reserved_seats_set = models.ManyToManyField("Ticket", blank=True)

    def get_available_seats(self):
        total_seats = self.hall.size
        reserved_seats = Ticket.objects.filter(session=self).count()
        available_seats = total_seats - reserved_seats
        return available_seats

    @property
    def available_seats(self):
        return self.get_available_seats()

    def reserve_seat(self, user, seat_number):
        if self.available_seats <= 0:
            return False

        existing_ticket = Ticket.objects.filter(session=self, seat_number=seat_number).first()
        if existing_ticket:
            return False

        ticket_price = self.ticket_price
        ticket = Ticket.objects.create(session=self, seat_number=seat_number, user=user, price=ticket_price)

        self.reserved_seats += 1
        self.save()

        return ticket

    def __str__(self):
        return f"{self.movie.title} - {self.start_date} - {self.start_time}"


class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.session.movie.title} - Seat {self.seat_number}"
