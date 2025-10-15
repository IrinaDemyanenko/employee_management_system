"""Тесты IsAdminOrReadOnly."""
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from employees.permissions import IsAdminOrReadOnly
from django.contrib.auth import get_user_model

User = get_user_model()

class PermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_is_allowed_for_all(self):
        request = self.factory.get("/api/workers/")
        perm = IsAdminOrReadOnly()
        self.assertTrue(perm.has_permission(request, None))

    def test_post_denied_for_non_admin(self):
        user = User.objects.create_user("user")
        request = self.factory.post("/api/workers/")
        request.user = user
        perm = IsAdminOrReadOnly()
        self.assertFalse(perm.has_permission(request, None))
