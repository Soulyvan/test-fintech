from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Wallet

User = get_user_model()


class WalletTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="alice",
            password="test1234"
        )

        self.wallet = Wallet.objects.create(
            owner=self.user,
            balance=0
        )

    def authenticate(self):
        response = self.client.post("/api/auth/login/", {
            "username": "alice",
            "password": "test1234"
        })

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_deposit(self):
        self.authenticate()

        response = self.client.post("/api/wallet/deposit/", {
            "amount": 1000
        })

        self.wallet.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.wallet.balance, 1000)

    def test_transfer(self):
        user2 = User.objects.create_user(
            username="bob",
            password="test1234"
        )

        Wallet.objects.create(owner=user2, balance=0)

        self.authenticate()

        response = self.client.post("/api/wallet/transfer/", {
            "recipient_id": user2.id,
            "amount": 500
        })

        self.wallet.refresh_from_db()
        user2.wallet.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.wallet.balance, 500)
        self.assertEqual(user2.wallet.balance, 500)