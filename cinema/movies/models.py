from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField()
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.title
