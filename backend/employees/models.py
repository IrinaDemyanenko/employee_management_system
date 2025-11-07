from django.db import models
from django.conf import settings


class Worker(models.Model):
    """Описывает работника."""

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    position = models.CharField(max_length=200, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    hired_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_employees",
    )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-hired_date"]

    def __str__(self):
        return f"""
    ФИО: {self.last_name} {self.middle_name} {self.first_name},
    Должность: {self.position},
    Создан: {self.created_by}
    """
