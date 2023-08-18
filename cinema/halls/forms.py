from django import forms
from .models import MovieSession, CinemaHall, Ticket


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


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['reservation_date', 'seat']
