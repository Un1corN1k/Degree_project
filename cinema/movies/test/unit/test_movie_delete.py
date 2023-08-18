from django.test import TestCase, Client
from django.urls import reverse
from movies.models import Movie
from accounts.models import CustomUser


class MovieDeleteViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='adminpassword')
        self.client = Client()

        self.movie = Movie.objects.create(
            title="Movie 2",
            price=5,
            description="Description for Movie 2",
            release_date="2023-07-15",
            duration=105,
            poster="posters/movie2.jpg"
        )

    def test_logged_in_admin_can_access_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('movie_delete', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_confirm_delete.html')

    def test_non_admin_cannot_access_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('movie_delete', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 403)

    def test_form_submission(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('movie_delete', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.count(), 0)
