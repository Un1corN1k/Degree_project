from django.db import models
from django.conf import settings


class Movie(models.Model):
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.title
