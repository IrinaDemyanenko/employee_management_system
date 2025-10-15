"""Тесты GET /api/workers/, GET /api/workers/{id}/."""
from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Worker


class WorkerListDetailTests(APITestCase):
    def setUp(self):
        self.worker = Worker.objects.create(
            first_name="Анна", last_name="Смирнова",
            email="anna@example.com", position="HR"
        )

    def test_list_workers(self):
        response = self.client.get("/api/workers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Анна", str(response.data))

    def test_detail_worker(self):
        response = self.client.get(f"/api/workers/{self.worker.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("anna@example.com", str(response.data))
