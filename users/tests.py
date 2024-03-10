from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


# Create your tests here.
class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='normaluser', password='foo')
        self.assertEqual(user.username, 'normaluser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(username='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', password="foo")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser('superuser', 'foo')
        self.assertEqual(admin_user.username, 'superuser')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='superuser', password='foo', is_superuser=False)


class UserAPITestCase(APITestCase):
    def test_register_new_user(self):
        test_user = {
            'username': 'test',
            'password': 'Arstdhneio123'
        }

        initial_count = User.objects.count()
        response = self.client.post('/api/sign-up/', data=test_user, format='json')
        new_count = User.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_count, initial_count + 1)
