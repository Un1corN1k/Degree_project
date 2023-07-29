from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from .forms import MovieSessionForm, CinemaHallForm, ReserveSeatForm
from .models import CinemaHall, MovieSession, Ticket
from movies.models import Movie


class CinemaHallListView(ListView):
    model = CinemaHall
    template_name = 'halls/cinema_hall_list.html'
    context_object_name = 'halls'


class CinemaHallCreateView(CreateView):
    model = CinemaHall
    form_class = CinemaHallForm
    template_name = 'halls/cinema_hall_create.html'
    success_url = reverse_lazy('cinema_hall_list')


class MovieSessionListView(ListView):
    model = MovieSession
    template_name = 'halls/movie_session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        sessions = MovieSession.objects.select_related('movie', 'hall')
        for session in sessions:
            session.available_seats = session.get_available_seats()
        return sessions


class MovieSessionDetailView(DetailView):
    model = MovieSession
    template_name = 'halls/movie_session_detail.html'
    context_object_name = 'session'

    def get(self, request, *args, **kwargs):
        session = self.get_object()
        if session.reserve_seat():
            return render(request, 'halls/seat_reserved.html', {'session': session})
        else:
            return render(request, 'halls/no_seats_available.html', {'session': session})


def create_movie_session(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = MovieSessionForm(request.POST)
        if form.is_valid():
            hall = form.cleaned_data['hall']
            movie = form.cleaned_data['movie']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            overlapping_sessions = MovieSession.objects.filter(
                hall=hall,
                start_date__lte=start_date,
                end_date__gte=end_date,
            )

            for session in overlapping_sessions:
                if (
                    (start_time >= session.start_time and start_time <= session.end_time) or
                    (end_time >= session.start_time and end_time <= session.end_time) or
                    (start_time <= session.start_time and end_time >= session.end_time)
                ):
                    return render(request, 'halls/error.html', {'message': 'Сеанс перекривається з іншим сеансом в залі.'})

            form.save()
            return redirect('movie-session-list')
    else:
        form = MovieSessionForm()

    halls = CinemaHall.objects.all()
    movies = Movie.objects.all()
    return render(request, 'halls/create_movie_session.html', {'form': form, 'halls': halls, 'movies': movies})


def movie_session_list(request):
    sessions = MovieSession.objects.all()
    return render(request, 'halls/movie_session_list.html', {'sessions': sessions})


def reserve_seat(request, session_id):
    session = get_object_or_404(MovieSession, pk=session_id)

    if request.method == 'POST':
        seat_number = int(request.POST.get('seat_number', 0))
        if session.reserve_seat(request.user, seat_number):
            return render(request, 'halls/seat_reserved.html', {'session': session})
        else:
            return render(request, 'halls/no_seats_available.html', {'session': session})

    return render(request, 'halls/reserve_seat.html', {'session': session})


def seat_reserved(request, session_id):
    session = get_object_or_404(MovieSession, pk=session_id)
    return render(request, 'halls/seat_reserved.html', {'session': session})