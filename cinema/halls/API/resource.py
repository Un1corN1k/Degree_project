from datetime import date, timedelta
from rest_framework import viewsets, status, generics
from halls.models import CinemaHall, MovieSession, Ticket
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CinemaHallSerializer, MovieSessionSerializer, TicketSerializer
from movies.API.permissions import IsSuperUserPermission
from movies.API.authorization import TokenExpired


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [IsAuthenticated, IsSuperUserPermission]
    authentication_classes = [TokenExpired, ]


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer
    permission_classes = [IsAuthenticated, IsSuperUserPermission]
    authentication_classes = [TokenExpired, ]


class ReserveSeatAPIView(APIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, movie_session_id):
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)
        today = date.today()

        available_dates = self.get_available_dates(movie_session, today)
        available_seats = list(range(1, movie_session.hall.size + 1))
        reserved_tickets = Ticket.objects.filter(movie_session=movie_session, reservation_date__in=available_dates)

        serializer = MovieSessionSerializer(movie_session)
        return Response({
            'movie_session': serializer.data,
            'available_dates': available_dates,
            'available_seats': available_seats,
            'reserved_tickets': TicketSerializer(reserved_tickets, many=True).data,
        })

    def post(self, request, movie_session_id):
        today = date.today()
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)
        available_seats = list(range(1, movie_session.hall.size + 1))
        reserved_seats = Ticket.objects.filter(movie_session=movie_session).values_list('seat', flat=True)
        available_dates = self.get_available_dates(movie_session, today)

        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            seat = serializer.validated_data['seat']
            reservation_date = serializer.validated_data['reservation_date']

            if reservation_date in available_dates and seat in available_seats and seat not in reserved_seats:
                ticket_price = movie_session.movie.price
                ticket = Ticket.objects.create(user=request.user, movie_session=movie_session, seat=seat,
                                               price=ticket_price, reservation_date=reservation_date)
                return Response({'message': 'Місце заброньовано'}, status=status.HTTP_201_CREATED)

            message = "Місце вже заброньовано або не доступно на цю дату."
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    def get_available_dates(self, movie_session, today):
        available_dates = [date for date in
                           (today + timedelta(days=i) for i in range((movie_session.end_date - today).days + 1)) if
                           date >= today]
        return available_dates


class SeatReservedAPIView(APIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, movie_session_id):
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)
        ticket = movie_session.ticket_set.last()

        if ticket:
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Місце ще не заброньовано'}, status=status.HTTP_404_NOT_FOUND)
