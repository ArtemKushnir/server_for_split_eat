from .data import restaurants
from .models import Category, Restaurant

BASE_URL = "https://eda.yandex.ru/r/"


def add_restaurants():
    for restaurant in restaurants:
        if Restaurant.objects.filter(name=restaurant["name"]).exists():
            continue
        restaurant["menu"] = BASE_URL + restaurant["menu"]
        categories_name = restaurant.pop("categories")
        restaurant_model = Restaurant(**restaurant)
        restaurant_model.save()
        categories = [Category.objects.get_or_create_singleton(category_name) for category_name in categories_name]
        restaurant_model.categories.add(*categories)
