"""Регистрация модели в админке."""
from django.contrib import admin
from django.test import TestCase
from employees.models import Worker
from employees.admin import WorkerAdmin

class AdminTests(TestCase):
    def test_worker_registered_in_admin(self):
        self.assertIn(Worker, admin.site._registry)

    def test_admin_config(self):
        worker_admin = admin.site._registry[Worker]
        self.assertIsInstance(worker_admin, WorkerAdmin)
        self.assertIn("is_active", worker_admin.list_editable)
