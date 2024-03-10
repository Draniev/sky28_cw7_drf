from django.urls import path, include
from rest_framework import routers

from habits.views import HabitCreateAPIView, HabitCRUDAPIView

router = routers.DefaultRouter()
router.register(r'habits', HabitCRUDAPIView, basename='habits')

urlpatterns = [
    path('', include(router.urls)),
    # path('habits/create/', HabitCreateAPIView.as_view(), name='create-habit'),
    # path('user/<int:pk>/', UserApiView.as_view(), name='user-api-view'),
]
