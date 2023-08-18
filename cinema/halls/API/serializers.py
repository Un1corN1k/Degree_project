from rest_framework import serializers
from halls.models import CinemaHall, MovieSession


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = '__all__'


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = '__all__'

    def validate(self, data):
        existing_sessions = MovieSession.objects.filter(
            hall=data['hall'],
            start_date=data['start_date'],
            end_date=data['end_date'],
        ).exclude(pk=self.instance.pk if self.instance else None)

        for session in existing_sessions:
            if (
                    (data['start_time'] < session.end_time and data['end_time'] > session.start_time)
                    or (data['start_time'] == session.start_time and data['end_time'] == session.end_time)
            ):
                raise serializers.ValidationError("Цей час показу перекривається з іншим показом.")
        return data


class TicketSerializer(serializers.Serializer):
    seat = serializers.IntegerField()
    reservation_date = serializers.DateField()
