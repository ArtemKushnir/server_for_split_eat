from django.contrib import admin

from .models import TrackedCart


@admin.register(TrackedCart)
class TrackedCartAdmin(admin.ModelAdmin):
    list_display = ("id", "display_carts", "status", "created_at")

    def display_carts(self, obj):
        return ", ".join([str(cart.id) for cart in obj.carts.all()])

    display_carts.short_description = "Корзины"
