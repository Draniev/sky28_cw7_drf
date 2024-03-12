from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bot.models import TgUser
from config.config import tg_client


class TgUserVerificationAPIView(APIView):
    def get(self, request, verification_code, *args, **kwargs):
        try:
            tg_user = TgUser.objects.get(verification_code=verification_code)
            tg_user.user = request.user
            tg_user.verification_code = None
            tg_user.save()

            keyboard = tg_client.create_keyboard()
            tg_client.send_message(tg_user.chat_id, "Вы успешно прошли верификацию!", reply_markup=keyboard)
            return Response({"message": "User verified successfully."}, status=status.HTTP_200_OK)
        except TgUser.DoesNotExist:
            return Response({"message": "Verification code is wrong."}, status=status.HTTP_400_BAD_REQUEST)