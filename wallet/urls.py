from django.urls import path
from .views import WalletDetailView, DepositView, TransferView, TransactionHistoryView

urlpatterns = [
    path("", WalletDetailView.as_view(), name="wallet-detail"),
    path("deposit/", DepositView.as_view()),
    path("transfer/", TransferView.as_view()),
    path("transactions/", TransactionHistoryView.as_view()),
]
