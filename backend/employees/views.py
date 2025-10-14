from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from employees.models import Worker
from employees.serializers import WorkerAllSerializer, WorkerDetailSerializer
from employees.permissions import IsAdminOrReadOnly


class WorkerViewSet(viewsets.ModelViewSet):
    """CRUD для модели Worker.

    GET /api/workers/ — список работников
    POST /api/workers/ — создание работника
    GET /api/workers/{id}/ — детальная информация
    PATCH /api/workers/{id}/ — обновление
    DELETE /api/workers/{id}/ — удаление
    """

    queryset = Worker.objects.all().select_related("created_by")
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active", "position"]

    def get_serializer_class(self):
        if self.action == "list":
            return WorkerAllSerializer
        return WorkerDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
