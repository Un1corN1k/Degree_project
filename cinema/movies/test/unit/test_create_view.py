from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from movies.models import Movie
from accounts.models import CustomUser
import json


class CreateMovieViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        cls.superuser = CustomUser.objects.create_superuser(username='admin', password='adminpassword')
        cls.client = Client()


    def test_logged_in_user_can_access_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('movie_create'))
        self.assertEqual(response.status_code, 403)


    def test_superuser_can_access_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('movie_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/create_movie.html')
