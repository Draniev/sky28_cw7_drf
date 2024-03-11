from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bot.models import TgUser


class TgUserVerificationAPIView(APIView):
    def get(self, request, verification_code, *args, **kwargs):
        try:
            tg_user = TgUser.objects.get(verification_code=verification_code)
            tg_user.user = request.user
            tg_user.verification_code = None
            tg_user.save()
            return Response({"message": "User verified successfully."}, status=status.HTTP_200_OK)
        except TgUser.DoesNotExist:
            return Response({"message": "Verification code is wrong."}, status=status.HTTP_400_BAD_REQUEST)