from django.db import models
from django.utils.timezone import now

from cart.models import Cart


class TrackedCart(models.Model):
    STATUS_CHOICES = ((True, "Matched"), (False, "Close"))

    carts = models.ManyToManyField(Cart, verbose_name="Корзины")
    status = models.BooleanField(choices=STATUS_CHOICES, default=True, verbose_name="Статус")
    created_at = models.DateTimeField(default=now, editable=False)
