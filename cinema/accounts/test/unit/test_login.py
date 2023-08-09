from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('user_login')

    def test_user_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_login.html')

    def test_user_login_view_post_success(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('home'))

    def test_user_login_view_post_failure(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_login.html')
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_user_login_view_redirect_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'))
