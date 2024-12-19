from django.db import models
from django.utils.timezone import now


class CartItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")

    def __str__(self):
        return self.name


class Cart(models.Model):
    products = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(default=now, editable=False)
