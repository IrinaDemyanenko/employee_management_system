from django.contrib import admin
from employees.models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    """Регулирует отображение модели Worker в админ-панели."""

    list_display = (
        'id', 'last_name', 'first_name', 'middle_name',
        'email', 'position', 'is_active', 'hired_date'
        )
    list_filter = ('is_active', 'position', 'hired_date')
    search_fields = (
        'first_name', 'last_name', 'middle_name', 'email', 'position'
        )
    list_editable = ('is_active',)
    readonly_fields = ('hired_date', 'updated', 'created_by')

    def save_model(self, request, obj, form, change):
        """Добавляет функционал:
        - автоматически проставляет, кто создал сотрудника created_by;
        - выводит в консоль сообщение, когда и кем создаётся новый работник.
        """
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

        if change:
            print(
                f'Работник {obj.id} {obj.first_name} {obj.last_name} изменён '
                f'в админ-пенели пользователем {request.user}.'
            )
        else:
            print(
                f'Работник {obj.id} {obj.first_name} {obj.last_name} создан '
                f'в админ-пенели пользователем {request.user}.'
            )
