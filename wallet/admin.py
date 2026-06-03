from django.contrib import admin
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "balance", "created_at", "updated_at")
    search_fields = ("owner__username", "owner__email")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")

    ordering = ("-created_at",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction_type", "status", "amount", "sender", "recipient", "created_at")

    search_fields = ("sender__username", "recipient__username",)

    list_filter = ("transaction_type", "status", "created_at")

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)