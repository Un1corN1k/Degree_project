from django.test import TestCase
from django.urls import reverse
from movies.models import Movie


class MovieDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.movie = Movie.objects.create(
            title='Test Movie',
            price=100,
            description='Test description',
            release_date='2023-07-01',
            duration=120,
            poster="posters/movie2.jpg"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/movies/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('movie_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('movie_detail', kwargs={'pk': self.movie.pk}))
        self.assertTemplateUsed(response, 'movies/movie_detail.html')

    def test_view_displays_correct_movie_details(self):
        response = self.client.get(reverse('movie_detail', kwargs={'pk': self.movie.pk}))
        self.assertContains(response, self.movie.title)
        self.assertContains(response, self.movie.price)
        self.assertContains(response, self.movie.description)
        self.assertContains(response, self.movie.duration)
        self.assertContains(response, self.movie.poster)
