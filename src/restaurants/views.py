from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MenuCategory, Product, Restaurant, RestaurantCategory
from .serializers import RestaurantMenuSerializer, RestaurantSerializer


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
            restaurants = (
                Restaurant.objects.annotate(
                    similarity_name=TrigramSimilarity("name", search_text),
                    similarity_categories=TrigramSimilarity("categories__name", search_text),
                )
                .filter(Q(similarity_name__gt=0.3) | Q(similarity_categories__gt=0.2))
                .order_by("name", "-similarity_name", "-similarity_categories")
                .distinct("name")
            )

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
            products = (
                Product.objects.annotate(
                    similarity_name=TrigramSimilarity("name", search_text),
                    similarity_category=TrigramSimilarity("category__name", search_text),
                )
                .filter(Q(similarity_name__gt=0.2) | Q(similarity_category__gt=0.2))
                .order_by("-similarity_name", "-similarity_category")
            )
        else:
            products = Product.objects.filter(restaurant=restaurant)

        serializer = RestaurantMenuSerializer(products, many=True)
        return Response({"products": serializer.data}, status.HTTP_200_OK)
