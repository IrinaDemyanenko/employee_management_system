"""Доступ POST, PATCH, DELETE в зависимости от роли."""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Worker

User = get_user_model()

class WorkerCRUDTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin", password="1234", is_staff=True)
        self.user = User.objects.create_user("user", password="1234")
        self.url = "/api/workers/"

    def test_admin_can_create_worker(self):
        self.client.login(username="admin", password="1234")
        data = {"first_name": "Петр", "last_name": "Сидоров",
                "email": "petr@example.com", "position": "QA"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Worker.objects.count(), 1)

    def test_user_cannot_create_worker(self):
        self.client.login(username="user", password="1234")
        data = {"first_name": "Аня", "last_name": "Ким",
                "email": "anya@example.com", "position": "PM"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_created_by_is_filled(self):
        self.client.login(username="admin", password="1234")
        data = {"first_name": "Марк", "last_name": "Тимофеев",
                "email": "mark@example.com", "position": "Dev"}
        self.client.post(self.url, data)
        worker = Worker.objects.get(email="mark@example.com")
        self.assertEqual(worker.created_by, self.admin)
