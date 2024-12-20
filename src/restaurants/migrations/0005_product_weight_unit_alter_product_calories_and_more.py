# Generated by Django 5.1.3 on 2024-12-20 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0004_alter_product_calories_alter_product_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="weight_unit",
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="calories",
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="product",
            name="weight",
            field=models.FloatField(default=0, null=True),
        ),
    ]