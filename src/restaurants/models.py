from django.db import models


class RestaurantCategoryManager(models.Manager):
    def get_or_create_singleton(self, name):
        obj, created = self.get_or_create(name=name)
        return obj


class RestaurantCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = RestaurantCategoryManager()


class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    menu = models.JSONField()
    logo = models.URLField()
    free_shipping_price = models.IntegerField()
    categories = models.ManyToManyField(RestaurantCategory, related_name="restaurants")

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
