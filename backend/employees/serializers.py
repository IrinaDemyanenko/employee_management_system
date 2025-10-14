"""Сериализаторы для преобразования моделей в JSON."""
from rest_framework import serializers
from employees.models import Worker


class WorkerAllSerializer(serializers.ModelSerializer):
    """Для просмотра всех работников — только базовые поля."""

    class Meta:
        model = Worker
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'position', 'is_active')


class WorkerDetailSerializer(serializers.ModelSerializer):
    """Для просмотра одного работника — все поля модели."""

    created_by = serializers.StringRelatedField(read_only=True)  # __str__, а не id

    class Meta:
        model = Worker
        fields = '__all__'
        read_only_fields = ('created_by', 'hired_date', 'updated')
