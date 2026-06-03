from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Wallet(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet({self.owner.username})"


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        TRANSFER = "TRANSFER", "Transfer"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_transactions")
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="received_transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUCCESS)
    created_at = models.DateTimeField(auto_now_add=True)
