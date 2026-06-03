from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import WalletSerializer, DepositSerializer, TransferSerializer, TransactionSerializer
from .services import deposit, transfer_money


@extend_schema(
    summary="Consulter son wallet",
    description="Retourne le solde et les informations du portefeuille de l'utilisateur connecté",
    responses=WalletSerializer
)
class WalletDetailView(RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet


@extend_schema(
    summary="Dépôt d'argent",
    description="Ajoute un montant au wallet de l'utilisateur connecté",
    request=DepositSerializer,
    responses={
        201: OpenApiResponse(description="Dépôt effectué avec succès")
    }
)
class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = request.user.wallet

        deposit(
            wallet=wallet,
            amount=serializer.validated_data['amount'],
        )

        return Response(
            {"message": "Dépôt effectué avec succès."},
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    summary="Transfert d'argent",
    description="Permet de transférer de l'argent vers un autre utilisateur",
    request=TransferSerializer,
    responses={
        200: OpenApiResponse(description="Transfert réussi"),
        400: OpenApiResponse(description="Erreur de validation ou solde insuffisant")
    }
)
class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            transaction = transfer_money(
                sender=request.user,
                recipient_id=serializer.validated_data["recipient_id"],
                amount=serializer.validated_data["amount"]
            )

            return Response({
                "message": "Transfert réussi",
                "transaction_id": transaction.id
            })

        except ValueError as e:
            return Response({"error": str(e)}, status=400)


@extend_schema(
    summary="Historique des transactions",
    description="Retourne toutes les transactions envoyées et reçues par l'utilisateur connecté",
    responses=TransactionSerializer(many=True)
)
class TransactionHistoryView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Transaction.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).select_related("sender", "recipient").order_by("-created_at")
