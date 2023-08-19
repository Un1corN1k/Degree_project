from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from .models import MovieSession, CinemaHall, Ticket


class CinemaHallForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = ['name', 'size', "poster"]


class MovieSessionForm(forms.ModelForm):
    class Meta:
        model = MovieSession
        fields = ['hall', 'movie', 'start_date', 'end_date', 'start_time', 'hall_reservation_to']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hall_reservation_to': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def calculate_end_time(self, start_time, movie_duration):
        start_datetime = datetime.combine(datetime.min.date(), start_time)
        end_datetime = start_datetime + timedelta(minutes=movie_duration)
        return end_datetime.time()

    def clean(self):
        cleaned_data = super().clean()
        hall = cleaned_data.get('hall')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        hall_reservation_to = cleaned_data.get('hall_reservation_to')

        conflicting_sessions = MovieSession.objects.filter(
            hall=hall,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exclude(pk=self.instance.pk)

        for session in conflicting_sessions:
            if session.start_date == start_date:
                if (session.start_time < hall_reservation_to and
                        session.hall_reservation_to > start_time):
                    raise ValidationError('This time overlaps with other film screenings in this cinema hall.')

            if session.start_date > start_date and session.start_date < end_date:
                if (session.start_time < hall_reservation_to and
                        session.hall_reservation_to > start_time):
                    raise ValidationError('This time overlaps with other film screenings in this cinema hall.')

        movie = cleaned_data.get('movie')
        if movie and start_time is not None:
            duration = movie.duration
            end_time = (datetime.combine(datetime.min.date(), start_time) +
                        timedelta(minutes=duration)).time()

            if hall_reservation_to < start_time:
                raise ValidationError('The time of booking the hall cannot be less than the start time of the movie.')

            if hall_reservation_to < end_time:
                raise ValidationError('The reservation time cannot be shorter than the duration of the movie.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        movie = self.cleaned_data.get('movie')
        start_time = self.cleaned_data.get('start_time')

        if movie and start_time is not None:
            duration = movie.duration
            instance.end_time = self.calculate_end_time(start_time, duration)

        if commit:
            instance.save()

        return instance


class TicketForm(forms.Form):
    seat = forms.IntegerField()
    reservation_date = forms.DateField()

    def __init__(self, *args, movie_session, available_seats, available_dates, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie_session = movie_session
        self.available_seats = available_seats
        self.available_dates = available_dates

    def clean(self):
        cleaned_data = super().clean()
        seat = cleaned_data.get('seat')
        reservation_date = cleaned_data.get('reservation_date')

        if reservation_date not in self.available_dates:
            raise ValidationError("Invalid reservation date")

        if seat not in self.available_seats:
            raise ValidationError("Invalid seat")

        if Ticket.objects.filter(movie_session=self.movie_session, reservation_date=reservation_date,
                                 seat=seat).exists():
            raise ValidationError("Seat already reserved")

        return cleaned_data
