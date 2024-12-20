from rest_framework import serializers

from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ["name", "menu", "logo", "free_shipping_price", "categories"]

    def get_categories(self, obj):
        return [category.name for category in obj.categories.all()]
