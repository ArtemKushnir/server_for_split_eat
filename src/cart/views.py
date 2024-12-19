from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import CartSerializer

# API для работы с корзиной пользователя
class CartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        cart_serializer = CartSerializer(data=request.data)
        if cart_serializer.is_valid():
            cart = cart_serializer.save()
            return Response(
                {"cart_id": cart.id, "message": "Корзина успешно создана."},
                status=status.HTTP_201_CREATED
            )
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)