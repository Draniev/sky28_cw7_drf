from django.contrib import admin
from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user', 'verification_code')
    search_fields = ('chat_id', 'user__username', 'verification_code')
    list_filter = ('user',)