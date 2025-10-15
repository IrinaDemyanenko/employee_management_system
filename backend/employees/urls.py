"""Эндпоинты API."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.views import WorkerViewSet
from employees.view_import import WorkerImportView


router = DefaultRouter()
router.register(r"workers", WorkerViewSet, basename="worker")

urlpatterns = [
    path('workers/import/', WorkerImportView.as_view(), name='worker-import'),
    path('', include(router.urls)),
]
