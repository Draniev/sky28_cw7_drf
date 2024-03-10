from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from habits.models import Habit
from habits.serializers import HabitCreateAPISerializer


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitCreateAPISerializer

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(owner=user)

