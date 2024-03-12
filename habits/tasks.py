from datetime import datetime, timedelta

from bot.models import TgUser
from config import celery_app
from config.config import tg_client
from habits.models import Habit


def get_habits_to_notify():
    current_day_of_week = datetime.now().weekday() + 1
    current_time = datetime.now().time()
    next_hour = (datetime.now() + timedelta(hours=1)).time()  # Вычисляем время через час (12 для тестов)

    habits_to_notify = Habit.objects.filter(schedule__id=current_day_of_week, time__range=(current_time, next_hour))

    return habits_to_notify


@celery_app.task()
def send_notifications():
    # print('Начали задачу по оповещению')
    habits_to_notify = get_habits_to_notify()
    # print(f'Всего требует оповещения: {len(habits_to_notify)}')

    for habit in habits_to_notify:
        # print(f'Задача {habit.name} от пользователя {habit.user.name}')
        tg_users = TgUser.objects.filter(user=habit.owner)

        for tg_user in tg_users:
            message = f"Сейчас тебе самое время {habit.name} в {habit.time} в {habit.place}"
            tg_client.send_message(tg_user.chat_id, message)
