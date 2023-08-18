from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from .forms import MovieSessionForm, CinemaHallForm, TicketForm
from .models import CinemaHall, MovieSession, Ticket
from movies.models import Movie
from datetime import date, timedelta


class CinemaHallListView(ListView):
    model = CinemaHall
    template_name = 'halls/cinema_hall_list.html'
    context_object_name = 'halls'


class CinemaHallCreateView(CreateView):
    model = CinemaHall
    form_class = CinemaHallForm
    template_name = 'halls/cinema_hall_create.html'
    success_url = reverse_lazy('user_profile')


class MovieSessionListView(LoginRequiredMixin, ListView):
    model = MovieSession
    template_name = 'halls/movie_session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        today = date.today()
        sessions = MovieSession.objects.select_related('movie', 'hall').filter(end_date__gte=today)
        for movie_session in sessions:
            movie_session.available_seats = movie_session.get_available_seats()
        return sessions


class MovieSessionDetailView(DetailView):
    model = MovieSession
    template_name = 'halls/movie_session_detail.html'
    context_object_name = 'movie_session'


class CreateMovieSessionView(CreateView):
    model = MovieSession
    form_class = MovieSessionForm
    template_name = 'halls/create_movie_session.html'
    success_url = reverse_lazy('movie-session-list')

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            return redirect('home')

        hall = form.cleaned_data['hall']
        start_time = form.cleaned_data['start_time']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        overlapping_sessions = MovieSession.objects.filter(
            hall=hall,
            start_date__lte=start_date,
            end_date__gte=end_date,
        )

        for session in overlapping_sessions:
            if ((start_time >= session.start_time and start_time <= session.end_time) or (
                    start_time <= session.start_time)):
                return render(self.request, 'halls/error.html',
                              {'message': 'The session overlaps with another session in the hall. Please change the time'})

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['halls'] = CinemaHall.objects.all()
        context['movies'] = Movie.objects.all()
        return context


class ReserveSeatView(View):
    def get(self, request, movie_session_id):
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)
        today = date.today()

        available_dates = [movie_session.start_date + timedelta(days=i) for i in
                           range((movie_session.end_date - movie_session.start_date).days + 1)
                           if movie_session.start_date + timedelta(days=i) >= today]

        available_seats = list(range(1, movie_session.hall.size + 1))
        reserved_tickets = Ticket.objects.filter(movie_session=movie_session, reservation_date__in=available_dates)

        form = TicketForm()
        return render(request, 'halls/reserve_seat.html',
                      {'movie_session': movie_session, 'form': form,
                       'available_dates': available_dates, 'available_seats': available_seats,
                       'reserved_tickets': reserved_tickets})

    def post(self, request, movie_session_id):
        today = date.today()
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)
        available_seats = list(range(1, movie_session.hall.size + 1))
        reserved_seats = Ticket.objects.filter(movie_session=movie_session).values_list('seat', flat=True)
        available_dates = [today + timedelta(days=i) for i in
                           range((movie_session.end_date - movie_session.start_date).days + 1)]

        form = TicketForm(request.POST)
        if form.is_valid():
            seat = form.cleaned_data['seat']
            reservation_date = form.cleaned_data['reservation_date']

            if reservation_date in available_dates and seat in available_seats and \
                    not Ticket.objects.filter(Q(reservation_date=reservation_date) & Q(seat=seat)).exists():
                ticket_price = movie_session.movie.price

                ticket = Ticket.objects.create(user=request.user, movie_session=movie_session, seat=seat,
                                               price=ticket_price, reservation_date=reservation_date)
                return redirect('seat_reserved', movie_session_id=movie_session_id)

        message = "Try a different seat or date."
        return render(request, 'halls/reserve_seat.html',
                      {'movie_session': movie_session, 'form': form,
                       'available_dates': available_dates, 'available_seats': available_seats,
                       'reserved_seats': reserved_seats, 'message': message})

    def get_available_dates(self, movie_session):
        today = date.today()
        available_dates = [date for date in
                           (today + timedelta(days=i) for i in range((movie_session.end_date - today).days + 1)) if
                           date >= today]

        return available_dates


class SeatReservedView(View):
    template_name = 'halls/seat_reserved.html'

    def get(self, request, movie_session_id):
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)
        ticket = movie_session.ticket_set.last()
        context = {'movie_session': movie_session, 'ticket': ticket}
        return render(request, self.template_name, context)
