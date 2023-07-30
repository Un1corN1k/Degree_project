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
        available_seats = total_seats - self.reserved_seats - self.booked_seats.count()
        return available_seats

    def get_available_seats_list(self):
        total_seats = self.hall.size
        available_seats = total_seats - self.reserved_seats
        return list(range(1, available_seats + 1))

    @property
    def available_seats(self):
        return self.get_available_seats()

    def reserve_seat(self, user, seat_number):
        if seat_number in self.booked_seats.values_list('seat_number', flat=True):
            return False

        ticket_price = self.ticket_price
        booked_seat = BookedSeat.objects.create(session=self, seat_number=seat_number)
        Ticket.objects.create(user=user, booked_seat=booked_seat, price=ticket_price)
        return True

    def __str__(self):
        return f"{self.movie.title} - {self.start_date} - {self.start_time}"


class BookedSeat(models.Model):
    session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.session} - Місце {self.seat_number}"


class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    booked_seat = models.ForeignKey(BookedSeat, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def seat_number(self):
        return self.booked_seat.seat_number if self.booked_seat else None

    @seat_number.setter
    def seat_number(self, value):
        if self.booked_seat:
            self.booked_seat.seat_number = value
            self.booked_seat.save()

    def __str__(self):
        return f"{self.user.username} - {self.session.movie.title} - Місце {self.seat_number}"
