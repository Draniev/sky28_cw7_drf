from django.urls import path

from bot.views import TgUserVerificationAPIView

urlpatterns = [
    path('verify/<str:verification_code>/', TgUserVerificationAPIView.as_view(), name='tg_user_verify'),
]
