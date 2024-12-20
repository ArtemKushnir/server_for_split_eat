from django.db import models


class CategoryManager(models.Manager):
    def get_or_create_singleton(self, name):
        obj, created = self.get_or_create(name=name)
        return obj


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = CategoryManager()


class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    menu = models.URLField()
    logo = models.URLField()
    free_shipping_price = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name="restaurants")
