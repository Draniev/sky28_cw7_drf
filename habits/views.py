from django.db.models import Q
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.serializers import HabitCreateAPISerializer, HabitAPIViewSerializer


class Paginator(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр запроса для указания количества элементов на странице
    max_page_size = 100  # Максимальное количество элементов на странице


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitCreateAPISerializer

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(owner=user)


class HabitCRUDAPIView(ModelViewSet):
    pagination_class = Paginator

    def get_queryset(self):
        user = self.request.user
        if self.action in ('list', 'retrieve'):
            queryset = Habit.objects.filter(Q(owner=user) | Q(is_public=True))
        else:
            queryset = Habit.objects.filter(owner=user)
        return queryset

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            serializer_class = HabitCreateAPISerializer
        else:
            serializer_class = HabitAPIViewSerializer
        return serializer_class
