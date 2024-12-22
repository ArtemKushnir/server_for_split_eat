from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MenuCategory, Restaurant, RestaurantCategory, Product
from .serializers import RestaurantSerializer, RestaurantMenuSerializer


class RestaurantPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class RestaurantsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category_name = request.query_params.get("category", None)
        search_text = request.query_params.get("search", None)
        if category_name:
            category = RestaurantCategory.objects.get(name=category_name)
            restaurants = Restaurant.objects.filter(categories=category)
        elif search_text:
            restaurants = Restaurant.objects.filter(name=search_text)
        else:
            restaurants = Restaurant.objects.all()

        paginator = RestaurantPagination()
        paginated_restaurants = paginator.paginate_queryset(restaurants, request)

        serializer = RestaurantSerializer(paginated_restaurants, many=True)

        return paginator.get_paginated_response(serializer.data)


class RestaurantCategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = {"categories": [category.name for category in RestaurantCategory.objects.all()]}
        return Response(categories, status=status.HTTP_200_OK)


class MenuCategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        restaurant_name = request.query_params.get("restaurant", None)
        if restaurant_name:
            restaurant = Restaurant.objects.get(name=restaurant_name)
            categories = {
                "categories": [category.name for category in MenuCategory.objects.filter(restaurant=restaurant)]
            }
            return Response(categories, status=status.HTTP_200_OK)


class RestaurantMenuListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        restaurant_name = request.query_params.get("restaurant")
        category_name = request.query_params.get("category", None)
        search_text = request.query_params.get("search", None)

        restaurant = Restaurant.objects.get(name=restaurant_name)
        if category_name:
            category = MenuCategory.objects.get(name=category_name, restaurant=restaurant)
            products = Product.objects.filter(restaurant=restaurant, category=category)
        elif search_text:
            products = Product.objects.filter(restaurant=restaurant, name=search_text)
        else:
            products = Product.objects.filter(restaurant=restaurant)

        serializer = RestaurantMenuSerializer(products, many=True)
        return Response({"products": serializer.data}, status.HTTP_200_OK)
