from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', "price", 'description', 'release_date', 'duration', 'poster']
        widgets = {
            'release_date': forms.DateInput(format='%d.%m.%Y', attrs={'placeholder': 'year-month-day'}),
        }
