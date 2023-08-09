from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import CustomUser
from halls.models import Ticket


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/user_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reserved_tickets'] = Ticket.objects.filter(user=self.request.user)
        return context


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    redirect_authenticated_user = True


class UserRegistrationView(CreateView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = 'home'


