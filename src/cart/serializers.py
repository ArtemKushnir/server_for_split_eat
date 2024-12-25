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


class ActiveOrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    status = serializers.CharField()
    restaurant = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'restaurant', 'products', 'total_price', 'status', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def get_user(self, obj):
        return obj.user.email

    def get_restaurant(self, obj):
        return obj.restaurant.name if obj.restaurant else None

    def get_products(self, obj):
        return [{"id_product": {"name": product.id_product.name, "image": product.id_product.image}, "quantity": str(product.quantity)} for product in obj.products.all()]
