from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MenuCategory, Restaurant, RestaurantCategory
from .serializers import RestaurantSerializer


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
            try:
                category = RestaurantCategory.objects.get(name=category_name)
                restaurants = Restaurant.objects.filter(categories=category)
            except RestaurantCategory.DoesNotExist:
                return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
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
        restaurant = request.query_params.get("restaurant")
