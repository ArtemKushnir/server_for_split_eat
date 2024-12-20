from django.contrib import admin

from .models import MenuCategory, Product, Restaurant, RestaurantCategory

# Register your models here.


@admin.register(RestaurantCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "free_shipping_price", "get_categories")
    search_fields = ("name",)
    list_filter = ("categories",)
    ordering = ("name",)

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = "Категории"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "category", "weight", "weight_unit", "calories")
    search_fields = ("name", "restaurant__name")
    list_filter = ("restaurant",)


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant")
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = ("restaurant",)
