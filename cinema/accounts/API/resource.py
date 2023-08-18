from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from halls.models import Ticket
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_serializer = UserSerializer(user)
        reserved_tickets = Ticket.objects.filter(user=user)
        ticket_data = []

        for ticket in reserved_tickets:
            if isinstance(ticket.seat, int):
                ticket_data.append({
                    'id': ticket.id,
                    'movie_session': ticket.movie_session.id,
                    'seat': ticket.seat,
                    'reservation_date': ticket.reservation_date,
                    'created_at': ticket.created_at,
                    'price': str(ticket.price),
                })

        context = {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'reserved_tickets': ticket_data,
        }

        return Response(context, status=status.HTTP_200_OK)


class LoginUserView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email
        })
