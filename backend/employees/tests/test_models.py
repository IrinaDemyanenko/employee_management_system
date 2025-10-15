"""Тести модели Worker."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from employees.models import Worker

User = get_user_model()

class WorkerModelTests(TestCase):
    def test_create_worker_and_defaults(self):
        user = User.objects.create_user(username="admin")
        worker = Worker.objects.create(
            first_name="Иван", last_name="Иванов",
            email="ivan@example.com", position="Developer",
            created_by=user
        )
        self.assertTrue(worker.is_active)
        self.assertIsNotNone(worker.hired_date)
        self.assertEqual(worker.created_by, user)

    def test_string_representation(self):
        worker = Worker(first_name="Иван", last_name="Иванов")
        self.assertEqual(str(worker), "Иванов Иван")
