from django.contrib import admin
from .models import Habit


class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'time', 'is_pleasant', 'is_public', 'reward', 'linked_habit', 'periodicity')
    list_filter = ('owner', 'time', 'is_pleasant', 'is_public')
    search_fields = ('name', 'place')


admin.site.register(Habit, HabitAdmin)
