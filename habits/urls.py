from django.urls import path

from habits.views import HabitCreateAPIView

urlpatterns = [
    path('habits/create/', HabitCreateAPIView.as_view(), name='create-habit'),
    # path('user/<int:pk>/', UserApiView.as_view(), name='user-api-view'),
]
