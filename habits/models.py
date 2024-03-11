from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Day(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)  # Содержание привычки
    place = models.CharField(max_length=100)
    time = models.TimeField()
    is_pleasant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    execution_seconds = models.PositiveIntegerField(default=60)  # Время на выполнение в секундах
    schedule = models.ManyToManyField(Day, related_name='habits', blank=True)  # Поле для выбора дней недели
    reward = models.CharField(max_length=100, blank=True, null=True)
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.name}'
