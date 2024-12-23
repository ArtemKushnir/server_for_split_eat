import json

import requests

from .data import restaurants
from .models import Restaurant, RestaurantCategory


def add_restaurants():
    for restaurant in restaurants:
        if Restaurant.objects.filter(name=restaurant["name"]).exists():
            continue
        restaurant["menu"] = json.loads(requests.get(restaurant["menu"]).text)
        categories_name = restaurant.pop("categories")
        restaurant_model = Restaurant(**restaurant)
        restaurant_model.save()
        categories = [
            RestaurantCategory.objects.get_or_create_singleton(category_name) for category_name in categories_name
        ]
        restaurant_model.categories.add(*categories)
