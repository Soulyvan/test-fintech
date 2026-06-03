from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Wallet, Transaction

User = get_user_model()


def create_wallet_for_user(user):
    Wallet.objects.create(owner=user)


def deposit(wallet, amount):
    wallet.balance += amount
    wallet.save()

    Transaction.objects.create(
        recipient=wallet.owner,
        amount=amount,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        status=Transaction.Status.SUCCESS
    )

    return wallet


@transaction.atomic
def transfer_money(sender, recipient_id, amount):
    if sender.id == recipient_id:
        raise ValueError("Impossible de transférer vers soi-même.")

    try:
        recipient = User.objects.select_related("wallet").get(id=recipient_id)
    except User.DoesNotExist:
        raise ValueError("Destinataire introuvable.")

    sender_wallet = sender.wallet
    recipient_wallet = recipient.wallet

    if sender_wallet.balance < amount:
        raise ValueError("Solde insuffisant.")

    # Débit / Crédit
    sender_wallet.balance -= amount
    recipient_wallet.balance += amount

    sender_wallet.save()
    recipient_wallet.save()

    # Transaction log
    return Transaction.objects.create(
        sender=sender,
        recipient=recipient,
        amount=amount,
        transaction_type=Transaction.TransactionType.TRANSFER,
        status=Transaction.Status.SUCCESS
    )
