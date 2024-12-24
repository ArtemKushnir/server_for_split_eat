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
    restaurant = serializers.CharField()
    products = CartItemSerializer(many=True)
    total_price = serializers.FloatField()

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["user"] = user

        restaurant_name = validated_data.pop("restaurant")
        restaurant, _ = Restaurant.objects.get_or_create(name=restaurant_name)
        validated_data["restaurant"] = restaurant

        products_data = validated_data.pop("products")
        cart = Cart.objects.create(**validated_data)
        for product_data in products_data:
            product_id = product_data.pop("id_product")
            quantity = product_data.pop("quantity")
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} does not exist.")

            cart_item = CartItem.objects.create(id_product=product, quantity=quantity)
            cart.products.add(cart_item)

        return cart

    class Meta:
        model = Cart
        fields = ["restaurant", "products", "total_price"]
