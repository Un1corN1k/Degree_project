from django import forms
from .models import MovieSession, CinemaHall


class CinemaHallForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = ['name', 'size', "poster"]


class MovieSessionForm(forms.ModelForm):
    class Meta:
        model = MovieSession
        fields = ['hall', 'movie', 'start_time', 'end_time', 'start_date', 'end_date', 'ticket_price']

        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class ReserveSeatForm(forms.Form):
    seat_number = forms.IntegerField(label='Місце', widget=forms.Select)

    def __init__(self, *args, **kwargs):
        available_seats_list = kwargs.pop('available_seats_list', [])
        super().__init__(*args, **kwargs)
        self.fields['seat_number'].widget.choices = [(seat, seat) for seat in available_seats_list]
