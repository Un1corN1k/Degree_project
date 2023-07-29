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


class LoginRegisterView(TemplateView):
    template_name = 'accounts/login_register.html'


@login_required
def user_profile(request):
    user = request.user
    reserved_tickets = Ticket.objects.filter(user=user)
    return render(request, 'accounts/user_profile.html', {'user': user, 'reserved_tickets': reserved_tickets})


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    redirect_authenticated_user = True


class UserRegistrationView(CreateView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = 'home'


