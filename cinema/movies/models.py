from django.core.validators import MinValueValidator
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(max_length=10000)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(validators=[MinValueValidator(5)])
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.title
