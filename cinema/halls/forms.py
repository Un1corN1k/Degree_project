from django import forms
from .models import MovieSession, CinemaHall


class CinemaHallForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = ['name', 'size', "poster"]


class MovieSessionForm(forms.ModelForm):
    class Meta:
        model = MovieSession
        fields = ['hall', 'movie', 'start_date', 'end_date', 'start_time']

        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class SeatReservationForm(forms.Form):
    seat_numbers = forms.MultipleChoiceField(choices=[], widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        available_seats = kwargs.pop('available_seats', [])
        super(SeatReservationForm, self).__init__(*args, **kwargs)
        self.fields['seat_numbers'].choices = [(seat_number, f'Місце {seat_number}') for seat_number in available_seats]


class TicketForm(forms.Form):
    seat_number = forms.IntegerField(label='Місце', min_value=1)