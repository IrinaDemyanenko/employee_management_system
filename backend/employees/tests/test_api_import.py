"""Тесты импорта из Excel."""
import tempfile
from openpyxl import Workbook
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Worker


User = get_user_model()


class WorkerImportTests(APITestCase):
    """Проверка импорта работников из Excel."""

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="1234",
            is_staff=True,
        )
        self.url = "/api/workers/import/"


    def _create_excel_file(self, rows):
        """Создаёт временный Excel-файл с данными."""
        wb = Workbook()
        ws = wb.active
        ws.append(["first_name", "middle_name", "last_name", "email", "position"])  # заголовок
        for row in rows:
            ws.append(row)
        tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        wb.save(tmp.name)
        tmp.seek(0)
        return tmp


    def test_import_without_file(self):
        """Если файл не передан — возвращается ошибка 400."""
        self.client.login(username="admin", password="1234")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Файл не передан", str(response.data))


    def test_import_valid_excel(self):
        """Корректный Excel → 2 сотрудника созданы, ошибок нет."""
        self.client.login(username="admin", password="1234")

        rows = [
            ["Макар", "Никанурович", "Бехтерев", "bext@ya.ru", "сварщик"],
            ["Мария", None, "Лапухина", "lopyx@rambler.com", "менеджер"],
        ]
        tmp = self._create_excel_file(rows)

        response = self.client.post(self.url, {"file": tmp}, format="multipart")
        tmp.close()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Проверяем отчёт
        self.assertEqual(data["created"], 2)
        self.assertEqual(data["errors_count"], 0)
        self.assertEqual(len(data["errors"]), 0)

        # Проверяем, что записи созданы
        self.assertEqual(Worker.objects.count(), 2)
        self.assertTrue(Worker.objects.filter(email="bext@ya.ru").exists())


    def test_import_missing_required_fields(self):
        """Строки с пропущенными обязательными полями не импортируются."""
        self.client.login(username="admin", password="1234")

        rows = [
            ["Иван", "", "Иванов", "ivan@example.com", "Developer"],
            ["", "Александрович", "Петров", "", "QA"],  # отсутствует имя и email
        ]
        tmp = self._create_excel_file(rows)

        response = self.client.post(self.url, {"file": tmp}, format="multipart")
        tmp.close()

        data = response.json()
        self.assertEqual(data["created"], 1)
        self.assertEqual(data["errors_count"], 1)
        self.assertIn("отсутствуют обязательные поля", " ".join(data["errors"]))


    def test_import_invalid_email(self):
        """Некорректный email не проходит валидацию."""
        self.client.login(username="admin", password="1234")

        rows = [
            ["Олег", "", "Сидоров", "oleg@@example.com", "инженер"],  # двойное @
        ]
        tmp = self._create_excel_file(rows)

        response = self.client.post(self.url, {"file": tmp}, format="multipart")
        tmp.close()

        data = response.json()
        self.assertEqual(data["created"], 0)
        self.assertEqual(data["errors_count"], 1)
        self.assertIn("некорректный email", " ".join(data["errors"]))


    def test_import_duplicate_email_in_db(self):
        """Если email уже есть в БД — строка пропускается."""
        self.client.login(username="admin", password="1234")

        Worker.objects.create(
            first_name="Иван",
            last_name="Иванов",
            email="ivan@example.com",
            position="разработчик",
            created_by=self.admin,
        )

        rows = [
            ["Иван", "", "Иванов", "ivan@example.com", "разработчик"],  # дубликат в БД
        ]
        tmp = self._create_excel_file(rows)

        response = self.client.post(self.url, {"file": tmp}, format="multipart")
        tmp.close()

        data = response.json()
        self.assertEqual(data["created"], 0)
        self.assertEqual(data["errors_count"], 1)
        self.assertIn("дубликат email", " ".join(data["errors"]))


    def test_import_duplicate_email_in_file(self):
        """Если в Excel встречается один и тот же email — создаётся только первая запись."""
        self.client.login(username="admin", password="1234")

        rows = [
            ["Анна", "", "Соколова", "anna@example.com", "HR"],
            ["Аня", "", "Соколова", "anna@example.com", "HR"],  # дубликат в файле
        ]
        tmp = self._create_excel_file(rows)

        response = self.client.post(self.url, {"file": tmp}, format="multipart")
        tmp.close()

        data = response.json()
        self.assertEqual(data["created"], 1)
        self.assertEqual(data["errors_count"], 1)
        self.assertIn("дубликат email", " ".join(data["errors"]))
        self.assertEqual(Worker.objects.count(), 1)
