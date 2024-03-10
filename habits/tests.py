import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from habits.models import Habit

User = get_user_model()


class CreateHabitTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user', password='password123'
        )
        self.another_user = User.objects.create_user(
            username='another_user', password='password123'
        )
        self.test_user_pleasant_habit = Habit.objects.create(
            owner=self.test_user,
            name='test user pleasant_habit',
            place='some place',
            time=datetime.time(hour=12, minute=15),
            is_pleasant=True,
            is_public=True,
            execution_seconds=60,
            periodicity=Habit.Periodicity.daily,
        )
        self.test_user_not_pleasant_habit = Habit.objects.create(
            owner=self.test_user,
            name='test user pleasant_habit',
            place='some place',
            time=datetime.time(hour=12, minute=30),
            is_pleasant=False,
            is_public=True,
            execution_seconds=60,
            periodicity=Habit.Periodicity.daily,
        )
        self.another_user_pleasant_habit = Habit.objects.create(
            owner=self.another_user,
            name='another user pleasant_habit',
            place='some place',
            time=datetime.time(hour=12, minute=45),
            is_pleasant=True,
            is_public=True,
            execution_seconds=60,
            periodicity=Habit.Periodicity.daily,
        )

    def test_create_habit(self):
        self.client.force_authenticate(user=self.test_user)
        initial_count = Habit.objects.count()

        test_data = {
            'name': 'test habit',
            'place': 'test place',
            'time': '12:30:00',
        }
        response = self.client.post(
            '/api/habits/create/', data=test_data, format='json',
        )
        new_count = Habit.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_count, initial_count + 1)

    def test_create_habit_with_reward(self):
        self.client.force_authenticate(user=self.test_user)
        initial_count = Habit.objects.count()

        # Normal case Reward
        test_data = {
            'name': 'test habit',
            'place': 'test place',
            'time': '12:30:00',
            'reward': 'some reward',
        }
        response = self.client.post(
            '/api/habits/create/', data=test_data, format='json',
        )
        new_count = Habit.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_count, initial_count + 1)

        # Normal case Linked habit
        test_data = {
            'name': 'test habit',
            'place': 'test place',
            'time': '12:30:00',
            'linked_habit': self.test_user_pleasant_habit.id,
        }
        response = self.client.post(
            '/api/habits/create/', data=test_data, format='json',
        )
        new_count = Habit.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_count, initial_count + 2)

        # ERROR case Reward and Linked habit
        test_data = {
            'name': 'test habit',
            'place': 'test place',
            'time': '12:30:00',
            'reward': 'some reward',
            'linked_habit': self.test_user_pleasant_habit.id,
        }
        response = self.client.post(
            '/api/habits/create/', data=test_data, format='json',
        )
        new_count = Habit.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(new_count, initial_count + 2)

        # ERROR case Linked habit is not pleasant
        test_data = {
            'name': 'test habit',
            'place': 'test place',
            'time': '12:30:00',
            'linked_habit': self.test_user_not_pleasant_habit.id,
        }
        response = self.client.post(
            '/api/habits/create/', data=test_data, format='json',
        )
        new_count = Habit.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(new_count, initial_count + 2)

        # ERROR case Linked habit is not ownership for current user
        test_data = {
            'name': 'test habit',
            'place': 'test place',
            'time': '12:30:00',
            'linked_habit': self.another_user_pleasant_habit.id
        }
        response = self.client.post(
            '/api/habits/create/', data=test_data, format='json',
        )
        new_count = Habit.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(new_count, initial_count + 2)


