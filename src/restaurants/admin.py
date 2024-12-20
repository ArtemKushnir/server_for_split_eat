from django.contrib import admin

from .models import Category, Restaurant

# Register your models here.


@admin.register(Category)
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
