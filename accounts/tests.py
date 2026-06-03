from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        payload = {
            "username": "alice",
            "email": "alice@test.com",
            "password": "test1234"
        }

        response = self.client.post("/api/auth/register/", payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_login_user(self):
        User.objects.create_user(
            username="alice",
            email="alice@test.com",
            password="test1234"
        )

        response = self.client.post("/api/auth/login/", {
            "username": "alice",
            "password": "test1234"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)