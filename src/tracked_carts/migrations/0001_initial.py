# Generated by Django 5.1.3 on 2024-12-24 17:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrackedCart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.BooleanField(default=False, verbose_name="Статус")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("carts", models.ManyToManyField(to="cart.cart", verbose_name="Корзины")),
            ],
        ),
    ]
