from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movie
        fields = '__all__'
