from django.urls import path
from .views import UserLoginView, UserProfileView, UserLogoutView, UserRegistrationView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('registration/', UserRegistrationView.as_view(), name='user_registration'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
