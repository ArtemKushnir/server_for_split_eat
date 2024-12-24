# Generated by Django 5.1.3 on 2024-12-22 02:27

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("restaurants", "0013_menucategory_name_menu_category_gin_index"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="restaurantcategory",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["name"], name="category_name_gin_idx", opclasses=["gin_trgm_ops"]
            ),
        ),
    ]