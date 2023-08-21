from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView
from .forms import MovieSessionForm, CinemaHallForm, TicketForm
from .models import CinemaHall, MovieSession, Ticket
from datetime import date, timedelta
from movies.API.permissions import IsSuperUserMixin


class CinemaHallListView(ListView):
    model = CinemaHall
    template_name = 'halls/cinema_hall_list.html'
    context_object_name = 'halls'


class CinemaHallCreateView(IsSuperUserMixin, CreateView):
    model = CinemaHall
    form_class = CinemaHallForm
    template_name = 'halls/cinema_hall_create.html'
    success_url = reverse_lazy('cinema-hall-list')


class CinemaHallUpdateView(IsSuperUserMixin, UpdateView):
    model = CinemaHall
    form_class = CinemaHallForm
    template_name = 'halls/cinema_hall_update.html'
    context_object_name = 'hall'
    success_url = reverse_lazy('cinema-hall-list')


class CinemaHallDeleteView(IsSuperUserMixin, DeleteView):
    model = CinemaHall
    template_name = 'halls/cinema_hall_delete.html'
    context_object_name = 'hall'
    success_url = reverse_lazy('cinema-hall-list')


class MovieSessionListView(LoginRequiredMixin, ListView):
    model = MovieSession
    template_name = 'halls/movie_session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        today = date.today()
        sessions = MovieSession.objects.select_related('movie', 'hall').filter(end_date__gte=today)
        return sessions


class MovieSessionDetailView(DetailView):
    model = MovieSession
    template_name = 'halls/movie_session_detail.html'
    context_object_name = 'movie_session'


class MovieSessionDeleteView(IsSuperUserMixin, DeleteView):
    model = MovieSession
    template_name = 'halls/movie_session_delete.html'
    context_object_name = 'movie_session'
    success_url = reverse_lazy('movie-session-list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.ticket_set.exists():
            return render(request, 'halls/unavailable_update_template.html')
        return super().dispatch(request, *args, **kwargs)


class MovieSessionUpdateView(IsSuperUserMixin, LoginRequiredMixin, UpdateView):
    model = MovieSession
    form_class = MovieSessionForm
    template_name = 'halls/update_movie_session.html'
    success_url = reverse_lazy('movie-session-list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.ticket_set.exists():
            return render(request, 'halls/unavailable_update_template.html')
        return super().dispatch(request, *args, **kwargs)


class CreateMovieSessionView(IsSuperUserMixin, LoginRequiredMixin, CreateView):
    model = MovieSession
    form_class = MovieSessionForm
    template_name = 'halls/create_movie_session.html'
    success_url = reverse_lazy('movie-session-list')


class ReserveSeatView(FormView):
    template_name = 'halls/reserve_seat.html'
    form_class = TicketForm

    def get(self, request, *args, **kwargs):
        movie_session_id = kwargs['movie_session_id']
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)

        available_dates = self.get_available_dates(movie_session)

        available_seats = list(range(1, movie_session.hall.size + 1))
        reserved_tickets = Ticket.objects.filter(movie_session=movie_session, reservation_date__in=available_dates)

        form = self.form_class(movie_session=movie_session, available_seats=available_seats,
                               available_dates=available_dates)
        return self.render_to_response(
            {'movie_session': movie_session, 'form': form,
             'available_dates': available_dates, 'available_seats': available_seats,
             'reserved_tickets': reserved_tickets}
        )

    def post(self, request, *args, **kwargs):
        movie_session_id = kwargs['movie_session_id']
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)
        available_seats = list(range(1, movie_session.hall.size + 1))

        available_dates = self.get_available_dates(movie_session)

        form = self.form_class(request.POST, movie_session=movie_session, available_seats=available_seats,
                               available_dates=available_dates)
        if form.is_valid():
            seat = form.cleaned_data['seat']
            reservation_date = form.cleaned_data['reservation_date']
            ticket_price = movie_session.movie.price

            ticket = Ticket.objects.create(user=request.user, movie_session=movie_session, seat=seat,
                                           price=ticket_price, reservation_date=reservation_date)
            return redirect('seat_reserved', movie_session_id=movie_session_id)

        reserved_seats = Ticket.objects.filter(movie_session=movie_session).values_list('seat', flat=True)
        message = "Try a different seat or date."
        return self.render_to_response(
            {'movie_session': movie_session, 'form': form,
             'available_dates': available_dates, 'available_seats': available_seats,
             'reserved_seats': reserved_seats, 'message': message}
        )

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
