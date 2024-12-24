from django.db import models
from django.utils.timezone import now

from restaurants.models import Product, Restaurant

# from src.authentication.models import CustomUser


class CartItem(models.Model):
    id_product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")


class Cart(models.Model):
    STATUS_CHOICES = ((None, "Not matched"), (True, "Matched"), (False, "Close"))

    # user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    restaurant = models.ForeignKey(
        to=Restaurant, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ресторан"
    )
    products = models.ManyToManyField(CartItem)
    total_price = models.FloatField(null=True, blank=True, verbose_name="Общая сумма корзины")
    status = models.BooleanField(null=True, default=None, choices=STATUS_CHOICES, verbose_name="Статус корзины")
    created_at = models.DateTimeField(default=now, editable=False)
