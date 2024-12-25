import logging

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser

from .models import Cart
from .serializers import ActiveOrderSerializer, CartSerializer


class CartPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        cart_serializer = CartSerializer(data=request.data, context={"request": request})
        if cart_serializer.is_valid():
            cart = cart_serializer.save()
            return Response({"cart_id": cart.id, "message": "Корзина успешно создана."}, status=status.HTTP_201_CREATED)
        logger.error(f"Cart creation failed: {cart_serializer.errors}")
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


logger = logging.getLogger(__name__)
STATUS_CHOICES = {"None": None, "True": True, "False": False}


class ActiveUserOrdersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_name = request.query_params.get("user")
        status_name = request.query_params.get("status")

        logger.info(f"Received request with user: {user_name}, status: {status_name}")

        if not user_name:
            return Response({"error": "User parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not status_name:
            return Response({"error": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        if status_name == "None":
            status_value = None
        else:
            status_value = STATUS_CHOICES.get(status_name)

        logger.info(f"Status value after transformation: {status_value}")

        if status_value is None and status_name != "None":
            logger.info(f"Invalid status parameter: {status_name}")
            return Response({"error": "Invalid status parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=user_name)
            logger.info(f"Found user: {user}")

            carts = Cart.objects.filter(user=user, status=status_value)
            logger.info(f"QuerySet: {carts.query}")
            logger.info(f"Carts found: {carts}")

            serializer = ActiveOrderSerializer(carts, many=True)
            return Response({"carts": serializer.data}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            logger.info(f"User with email {user_name} not found")
            return Response({"error": "User with this email not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompletedUserOrderView:
    pass


# class AdminOrdersView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request):
#         user_name = request.query_params.get("user", None)
#         status_name = request.query_params.get("status", None)
#         if user_name:
#             user = Cart.objects.get(name=user_name)
#             status = Cart.objects.get(status=status_name)
#             carts = Cart.objects.filter(user=user, status=status)
#             serializer = ActiveOrderSerializer(carts, many=True)
#             return Response(serializer.data, status.HTTP_200_OK)
