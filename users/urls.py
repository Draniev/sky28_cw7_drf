from django.urls import path

from users.views import UserCreateAPIView

urlpatterns = [
    path('sign-up/', UserCreateAPIView.as_view(), name='api-user-register')
    # path('user/<int:pk>/', UserApiView.as_view(), name='user-api-view'),
]