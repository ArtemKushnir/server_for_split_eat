# Generated by Django 5.1.3 on 2024-12-20 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0003_remove_product_description_product_calories_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="calories",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="weight",
            field=models.IntegerField(default=0, null=True),
        ),
    ]