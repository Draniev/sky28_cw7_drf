from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TgUser(models.Model):
    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"

    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, verbose_name="User",
                             null=True,
                             on_delete=models.CASCADE,
                             related_name='TgUsers')
    verification_code = models.CharField(verbose_name='Код авторизации',
                                         max_length=255, null=True)
