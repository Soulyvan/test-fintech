from django.contrib.auth import get_user_model
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, ViewAllAccountsSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = []

    @extend_schema(
        summary="Inscription utilisateur",
        description="Créer un nouveau compte utilisateur et générer automatiquement un wallet",
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Connexion utilisateur",
    description="Authentifie l'utilisateur et retourne access + refresh token + user info",
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    summary="Lister tous les utilisateurs",
    description="Retourne la liste des comptes utilisateurs",
    responses=ViewAllAccountsSerializer(many=True)
)
class ViewAllAccountsView(APIView):
    permission_classes = []

    def get(self, request):
        users = User.objects.all()
        serializer = ViewAllAccountsSerializer(users, many=True)

        return Response(serializer.data)