from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed


class TokenExpired(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key=key)
        if (timezone.now() - token.created).seconds > 240:
            token.delete()
            raise AuthenticationFailed("Token expired")
        return user, token
