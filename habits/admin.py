from django.contrib import admin
from .models import Habit


class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'time', 'display_days_of_week', 'is_pleasant', 'is_public', 'reward', 'linked_habit')
    list_filter = ('owner', 'time', 'is_pleasant', 'is_public')
    search_fields = ('name', 'place')

    def display_days_of_week(self, obj):
        return ", ".join([day.name for day in obj.schedule.all()])


admin.site.register(Habit, HabitAdmin)
