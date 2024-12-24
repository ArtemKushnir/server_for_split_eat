from rest_framework import serializers

from restaurants.models import Product, Restaurant

from .models import Cart, CartItem


# Сериализатор для CartItem
class CartItemSerializer(serializers.Serializer):
    id_product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id_product", "quantity"]


# Сериализатор для CartRequest
class CartSerializer(serializers.Serializer):
    restaurant = serializers.CharField()  # Название ресторана
    products = CartItemSerializer(many=True)  # Поле для массива объектов CartItem
    total_price = serializers.FloatField()  # Общая стоимость корзины

    def create(self, validated_data):
        restaurant_name = validated_data.pop("restaurant")

        # Ищем или создаём объект Restaurant
        restaurant, _ = Restaurant.objects.get_or_create(name=restaurant_name)

        # Добавляем объект Restaurant в validated_data
        validated_data["restaurant"] = restaurant

        # Извлекаем вложенные данные продуктов
        products_data = validated_data.pop("products")

        # Создаем объект Cart
        cart = Cart.objects.create(**validated_data)

        # Создаем или связываем продукты с корзиной
        for product_data in products_data:
            # Извлекаем id_product и количество
            product_id = product_data.pop("id_product")
            quantity = product_data.pop("quantity")

            # Получаем объект Product
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} does not exist.")

            # Создаём CartItem
            cart_item = CartItem.objects.create(id_product=product, quantity=quantity)
            cart.products.add(cart_item)

        return cart

    class Meta:
        model = Cart
        fields = ["restaurant", "products", "total_price"]
