"""Разрешения, которые используются во viewset, чтобы реализовать роли."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Администратор — полный доступ, остальные — только чтение."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS — всем
        return request.user and request.user.is_staff
