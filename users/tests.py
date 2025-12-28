from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class UserTestCase(APITestCase):

    def test_user_create(self):
        url = reverse("users:user_create")

        data = {
            "username": "test",
            "email": "test@test.ru",
            "password": "12345678",
            "telegram_chat_id": "12345"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertNotEqual(user.password, "12345678")  # пароль захеширован
        self.assertTrue(user.check_password("12345678"))

    def test_user_list_unauthorized(self):
        url = reverse("users:user_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_authorized(self):
        user = User.objects.create_user(
            username="test",
            email="auth@test.ru",
            password="1234"
        )

        self.client.force_authenticate(user=user)

        url = reverse("users:user_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        user = User.objects.create_user(
            username="test",
            email="update@test.ru",
            password="1234"
        )

        self.client.force_authenticate(user=user)

        url = reverse("users:user_update", args=[user.id])

        response = self.client.patch(
            url,
            {"telegram_chat_id": "77777"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.telegram_chat_id, "77777")

    def test_cannot_update_foreign_user(self):
        user1 = User.objects.create_user(
            username="u1",
            email="u1@test.ru",
            password="1234"
        )
        user2 = User.objects.create_user(
            username="u2",
            email="u2@test.ru",
            password="1234"
        )

        self.client.force_authenticate(user=user1)

        url = reverse("users:user_update", args=[user2.id])
        response = self.client.patch(url, {"telegram_chat_id": "999"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
