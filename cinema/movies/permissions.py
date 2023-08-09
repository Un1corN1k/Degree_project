from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.permissions import BasePermission


class IsUserSuperUser(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
