# Generated by Django 5.1.3 on 2024-12-24 13:08

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("restaurants", "0014_restaurantcategory_category_name_gin_idx"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Количество")),
                (
                    "id_product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="restaurants.product", verbose_name="Продукт"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("total_price", models.FloatField(blank=True, null=True, verbose_name="Общая сумма корзины")),
                (
                    "status",
                    models.BooleanField(
                        choices=[(None, "Not matched"), (True, "Matched"), (False, "Close")],
                        default=None,
                        null=True,
                        verbose_name="Статус корзины",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                (
                    "restaurant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restaurants.restaurant",
                        verbose_name="Ресторан",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
                ("products", models.ManyToManyField(to="cart.cartitem")),
            ],
        ),
    ]
