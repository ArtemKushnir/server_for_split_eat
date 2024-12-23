from django.contrib.postgres.indexes import GinIndex
from django.db import models


class RestaurantCategoryManager(models.Manager):
    def get_or_create_singleton(self, name):
        obj, created = self.get_or_create(name=name)
        return obj


class RestaurantCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = RestaurantCategoryManager()

    class Meta:
        indexes = [
            GinIndex(fields=["name"], name="category_name_gin_idx", opclasses=["gin_trgm_ops"]),
        ]


class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    menu = models.JSONField()
    logo = models.URLField()
    free_shipping_price = models.IntegerField()
    categories = models.ManyToManyField(RestaurantCategory, related_name="restaurants")

    class Meta:
        indexes = [
            GinIndex(fields=["name"], name="name_restaurant_gin_index", opclasses=["gin_trgm_ops"]),
        ]

    def __str__(self):
        return self.name


class MenuCategoryManager(models.Manager):
    def get_or_create_singleton(self, name, restaurant):
        obj, created = self.get_or_create(name=name, restaurant=restaurant)
        return obj


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("name", "restaurant")

        indexes = [
            GinIndex(fields=["name"], name="name_menu_category_gin_index", opclasses=["gin_trgm_ops"]),
        ]

    objects = MenuCategoryManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)
    image = models.URLField(null=True)
    price = models.FloatField()
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    weight = models.FloatField(default=0, null=True)
    weight_unit = models.CharField(null=True)
    calories = models.FloatField(default=0, null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["name"], name="name_product_gin_index", opclasses=["gin_trgm_ops"]),
        ]
