from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from halls.models import Ticket


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('user_profile')

    def test_user_profile_view_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_profile_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_profile.html')
        self.assertEqual(response.context['user'], self.user)

    def test_user_profile_view_context_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('reserved_tickets', response.context)
        self.assertEqual(list(response.context['reserved_tickets']), list(Ticket.objects.filter(user=self.user)))
