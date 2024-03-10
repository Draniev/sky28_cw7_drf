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
            name='test user pleasant habit',
            place='some place',
            time=datetime.time(hour=12, minute=15),
            is_pleasant=True,
            is_public=True,
        )
        self.test_user_not_pleasant_habit = Habit.objects.create(
            owner=self.test_user,
            name='test user not pleasant habit',
            place='some place',
            time=datetime.time(hour=12, minute=30),
            is_pleasant=False,
            is_public=True,
        )
        self.another_user_pleasant_habit = Habit.objects.create(
            owner=self.another_user,
            name='another user pleasant habit',
            place='some place',
            time=datetime.time(hour=12, minute=45),
            is_pleasant=True,
            is_public=True,
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
            '/api/habits/', data=test_data, format='json',
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
            '/api/habits/', data=test_data, format='json',
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
            '/api/habits/', data=test_data, format='json',
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
            '/api/habits/', data=test_data, format='json',
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
            '/api/habits/', data=test_data, format='json',
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
            '/api/habits/', data=test_data, format='json',
        )
        new_count = Habit.objects.count()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(new_count, initial_count + 2)


class HabitListUpdRetrDelTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user', password='password123'
        )
        self.another_user = User.objects.create_user(
            username='another_user', password='password123'
        )

        self.test_user_pleasant_habit = Habit.objects.create(
            owner=self.test_user,
            name='test user pleasant habit',
            place='some place',
            time=datetime.time(hour=12, minute=15),
            is_pleasant=True,
            is_public=True,
        )
        self.test_user_public_habit = Habit.objects.create(
            owner=self.test_user,
            name='test user public habit',
            place='some place',
            time=datetime.time(hour=12, minute=30),
            is_pleasant=False,
            is_public=True,
            linked_habit=self.test_user_pleasant_habit
        )
        self.test_user_personal_habit = Habit.objects.create(
            owner=self.test_user,
            name='test user personal habit',
            place='some place',
            time=datetime.time(hour=12, minute=30),
            is_pleasant=False,
            is_public=False,
            reward='some reward'
        )

        self.another_user_public_pleasant_habit = Habit.objects.create(
            owner=self.another_user,
            name='another user public pleasant habit',
            place='some place',
            time=datetime.time(hour=12, minute=45),
            is_pleasant=True,
            is_public=True,
        )
        self.another_user_personal_pleasant_habit = Habit.objects.create(
            owner=self.another_user,
            name='another user personal pleasant habit',
            place='some place',
            time=datetime.time(hour=12, minute=45),
            is_pleasant=True,
            is_public=False,
        )
        self.another_user_public_habit1 = Habit.objects.create(
            owner=self.another_user,
            name='another user public habit with public reward',
            place='some place',
            time=datetime.time(hour=12, minute=30),
            is_pleasant=False,
            is_public=True,
            linked_habit=self.another_user_public_pleasant_habit
        )
        self.another_user_public_habit2 = Habit.objects.create(
            owner=self.another_user,
            name='another user public habit with personal reward',
            place='some place',
            time=datetime.time(hour=12, minute=30),
            is_pleasant=False,
            is_public=True,
            linked_habit=self.another_user_personal_pleasant_habit
        )
        self.another_user_personal_habit = Habit.objects.create(
            owner=self.another_user,
            name='another user personal habit',
            place='some place',
            time=datetime.time(hour=12, minute=30),
            is_pleasant=False,
            is_public=False,
            reward='some reward'
        )

    def test_list_habit(self):
        self.client.force_authenticate(user=self.test_user)

        response = self.client.get(
            '/api/habits/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # The tests should work if pagination is on or off
        if 'count' in response.data:
            habits = response.data['results']
        else:
            habits = response.data
        # there are only 6 public Habits in setUp
        self.assertEqual(len(habits), 6)
        self.assertEqual(habits[-1]['linked_habit'], 'secret private habit')

    def test_retrieve_habit(self):
        self.client.force_authenticate(user=self.test_user)

        response = self.client.get(
            f'/api/habits/{self.test_user_pleasant_habit.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            f'/api/habits/{self.another_user_personal_habit.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(
            f'/api/habits/{self.another_user_public_habit2.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['linked_habit'], 'secret private habit')

    def test_partial_update_habit(self):
        self.client.force_authenticate(user=self.test_user)
        test_data = {
            'name': 'test habit',
            'place': 'test place',
        }

        response = self.client.patch(
            f'/api/habits/{self.test_user_public_habit.id}/',
            data=test_data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test habit')

        response = self.client.patch(
            f'/api/habits/{self.another_user_public_habit1.id}/',
            data=test_data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Тут я нашел уязвимость в безопасности "своей системы". Оказалось
        # что при частичном обновлении можно обойти валидатор LinkedHabitAndRewardValidator
        # который не позволяет одновременно быть и награде и ссылке.
        # Но прямо сейчас у меня нет идей как элегантно это обойти.
        test_data = {
            'reward': 'to pet a cat',
        }
        response = self.client.patch(
            f'/api/habits/{self.test_user_public_habit.id}/',
            data=test_data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_update_habit(self):
        self.client.force_authenticate(user=self.test_user)
        test_data = {
            'owner': 2,
            'name': 'test habit',
            'place': 'test place',
            'time': '10:00:00',
            'is_pleasant': False,
            'is_public': False,
            'reward': 'to pet a cat',
            'linked_habit': None,
            'execution_seconds': 30,
            'periodicity': 'hourly',
        }

        response = self.client.put(
            f'/api/habits/{self.test_user_public_habit.id}/',
            data=test_data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reward'], 'to pet a cat')

    def test_delete_habit(self):
        self.client.force_authenticate(user=self.test_user)

        response = self.client.delete(
            f'/api/habits/{self.test_user_public_habit.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(
            f'/api/habits/{self.another_user_public_habit1.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

