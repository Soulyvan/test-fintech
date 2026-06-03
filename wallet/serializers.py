from rest_framework import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Wallet
        fields = [
            "id",
            "owner",
            "balance",
            "created_at",
            "updated_at"
        ]


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Entrer un montant valide.")
        return value


class TransferSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Montant invalide.")
        return value


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.username", read_only=True)
    recipient = serializers.CharField(source="recipient.username", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "created_at",
            "transaction_type",
            "amount",
            "status",
            "sender",
            "recipient",
        ]
