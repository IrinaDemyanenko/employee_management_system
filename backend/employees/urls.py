"""Эндпоинты API."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.views import WorkerViewSet


router = DefaultRouter()
router.register(r"workers", WorkerViewSet, basename="worker")

urlpatterns = [
    path("", include(router.urls)),
]
