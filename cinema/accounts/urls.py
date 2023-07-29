from django.urls import path
from . import views

urlpatterns = [
    path('login_register/', views.LoginRegisterView.as_view(), name='login_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('registration/', views.UserRegistrationView.as_view(), name='user_registration'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/', views.user_profile, name='user_profile'),
]
