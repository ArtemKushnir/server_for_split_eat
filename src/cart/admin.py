from django.contrib import admin

from .models import Cart, CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id_product", "id_product__name", "id_product__restaurant", "quantity")
    search_fields = ("id_product__name",)
    list_filter = ("id_product",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "total_price", "status", "created_at")
    search_fields = ("restaurant__name",)
    list_filter = ("status", "restaurant", "created_at")
    filter_horizontal = ("products",)
