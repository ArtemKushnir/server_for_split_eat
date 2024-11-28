from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class BaseTask(models.Model):
    url = models.URLField()


class RestaurantParse(models.Model):
    task_id = models.ForeignKey(BaseTask, blank=True, null=True, on_delete=models.PROTECT)
    restaurant_name = models.CharField(max_length=30)
    menu = ArrayField(models.CharField(max_length=30), size=3)
