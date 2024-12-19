from rest_framework import serializers

from .models import Cart, CartItem


# Сериализатор для CartItem
class CartItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["name", "price", "quantity"]


# Сериализатор для CartRequest
class CartSerializer(serializers.Serializer):
    products = CartItemSerializer(many=True)  # Поле для массива объектов CartItem

    def create(self, validated_data):
        # Извлекаем вложенные данные продуктов
        products_data = validated_data.pop("products")

        # Создаем объект Cart
        cart = Cart.objects.create(**validated_data)

        # Создаем или связываем продукты с корзиной
        for product_data in products_data:
            product, created = CartItem.objects.get_or_create(**product_data)
            cart.products.add(product)

        return cart

    class Meta:
        model = Cart
        fields = ["products"]
