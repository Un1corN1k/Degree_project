from django.test import TestCase
from django.urls import reverse
from movies.models import Movie


class HomeListViewTest(TestCase):
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

    def test_home_view_with_search(self):
        response = self.client.get(reverse('home'), {'search': 'Movie 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie 1')
        self.assertNotContains(response, 'Movie 2')

    def test_home_view_with_sorting(self):
        response = self.client.get(reverse('home'), {'sort_order': 'price', 'sort_direction': 'asc'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie 1')
        self.assertContains(response, 'Movie 2')

        movies = response.context['movies']
        sorted_movies = sorted(movies, key=lambda x: x.title)

        self.assertEqual(sorted_movies, list(Movie.objects.all()), msg='Movies are not sorted correctly')

    def test_home_view_no_results(self):
        response = self.client.get(reverse('home'), {'search': 'Nonexistent Movie'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Такого фільму не знайдено, спробуйте з іншим')

    def test_home_view_no_sort_order(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        movies = response.context['movies']
        sorted_movies = sorted(movies, key=lambda x: x.title)

        self.assertQuerysetEqual(sorted_movies, Movie.objects.all(), ordered=False)

