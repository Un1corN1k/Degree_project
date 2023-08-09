from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user_registration')
        self.data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }

    def test_user_registration_view(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_registration_invalid_data(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_user_registration_redirect_authenticated_user(self):
        user = CustomUser.objects.create_user(username='existinguser', password='existingpassword')
        self.client.login(username='existinguser', password='existingpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
