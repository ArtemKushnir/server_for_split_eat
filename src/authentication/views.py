from operator import truediv

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, EmailConfirmation
from .serializers import EmailConfirmationSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.check_user(request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            email_confirmation = EmailConfirmation(email=user)
            email_confirmation.save()
            email_confirmation.send_email()
            return Response(
                {"message": "Пользователь создан и ожидает подтверждения почты"}, status=status.HTTP_201_CREATED
            )
        return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = EmailConfirmationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get("email")
        user = serializer.get_user(email)
        user.activate()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Почта подтверждена, пользователь теперь активен",
                "access": str(refresh),
                "refresh": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class GetStatusView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email", None)
        if email:
            user: CustomUser = CustomUser.objects.get(email=email)
            return Response({"is_staff": user.is_staff}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
