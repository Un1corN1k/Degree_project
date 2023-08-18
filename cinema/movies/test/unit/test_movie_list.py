from django.test import TestCase
from django.urls import reverse
from movies.models import Movie


class MovieListViewTest(TestCase):

    def setUp(self):
        Movie.objects.create(
            title="Movie 1",
            price=10,
            description="Description for Movie 1",
            release_date="2023-07-01",
            duration=120,
            poster="posters/movie1.jpg"
        )
        Movie.objects.create(
            title="Movie 2",
            price=5,
            description="Description for Movie 2",
            release_date="2023-07-15",
            duration=105,
            poster="posters/movie2.jpg"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('movie_list'))
        self.assertTemplateUsed(response, 'movies/movie_list.html')

    def test_view_sorts_by_date_asc(self):
        response = self.client.get(reverse('movie_list'), {'sort_order': 'date', 'sort_direction': 'asc'})
        movies = response.context['movies']
        self.assertEqual(list(movies), [Movie.objects.get(title='Movie 1'), Movie.objects.get(title='Movie 2')])

    def test_view_sorts_by_date_desc(self):
        response = self.client.get(reverse('movie_list'), {'sort_order': 'date', 'sort_direction': 'desc'})
        movies = response.context['movies']
        self.assertEqual(list(movies), [Movie.objects.get(title='Movie 2'), Movie.objects.get(title='Movie 1')])


    def test_movie_list_view_no_sort_order(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)

        movies = response.context['movies']
        sorted_movies = sorted(movies, key=lambda x: x.title)

        self.assertEqual(list(sorted_movies), list(Movie.objects.all()))