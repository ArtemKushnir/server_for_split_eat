from .models import MenuCategory, Product, Restaurant

BASE_URL = "https://eda.yandex"


def add_menu():
    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        categories = restaurant.menu["payload"]["categories"]
        for category in categories:
            category_name = category["name"]
            items = category["items"]
            for item in items:
                if Product.objects.filter(name=item["name"]).exists():
                    continue
                item_name = item["name"]
                price = item["price"]
                image_url = BASE_URL + item["picture"]["uri"] if "picture" in item else None
                weight = float(item["measure"]["value"]) if "measure" in item else None
                weight_unit = item["measure"]["measure_unit"] if "measure" in item else None
                calories = float(item["nutrients"]["calories"]["value"]) if "nutrients" in item else None
                category_model = MenuCategory.objects.get_or_create_singleton(name=category_name, restaurant=restaurant)
                product_model = Product(
                    name=item_name,
                    restaurant=restaurant,
                    image=image_url,
                    price=price,
                    weight=weight,
                    weight_unit=weight_unit,
                    calories=calories,
                    category=category_model,
                )

                product_model.save()
