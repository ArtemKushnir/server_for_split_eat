from rest_framework import serializers

from .models import Product, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ["id", "name", "menu", "logo", "free_shipping_price", "categories"]

    def get_categories(self, obj):
        return [category.name for category in obj.categories.all()]


class RestaurantMenuSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField

    class Meta:
        model = Product
        fields = ["id", "name", "image", "price", "weight", "weight_unit", "calories"]

    def get_category(self, obj):
        return obj.category.name
