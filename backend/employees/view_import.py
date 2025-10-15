from rest_framework import status, views
from rest_framework.response import Response
from employees.permissions import IsAdminOrReadOnly
from services.import_service import WorkerImportService


class WorkerImportView(views.APIView):
    """Импорт работников из Excel."""

    permission_classes = [IsAdminOrReadOnly]

    def post(self, request):
        excel_file = request.FILES.get("file")
        if not excel_file:
            return Response(
                {"error": "Файл не передан."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = WorkerImportService(user=request.user)
        result = service.import_from_excel(excel_file)
        return Response(result, status=status.HTTP_200_OK)
