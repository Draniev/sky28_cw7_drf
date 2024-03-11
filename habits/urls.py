from django.urls import path, include
from rest_framework import routers

from habits.views import HabitCRUDAPIView, MyHabitListAPIView

router = routers.DefaultRouter()
router.register(r'habits', HabitCRUDAPIView, basename='habits')

urlpatterns = [
    path('habits/my/', MyHabitListAPIView.as_view(), name='my_habits'),
    path('', include(router.urls)),
    # path('habits/create/', HabitCreateAPIView.as_view(), name='create-habit'),
]
