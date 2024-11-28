from django.contrib import admin
from .models import BaseTask, RestaurantParse
# Register your models here.


@admin.register(BaseTask)
class BaseTaskAdmin(admin.ModelAdmin):
    list_display = ['url']


@admin.register(RestaurantParse)
class RestaurantParseAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'restaurant_name', 'menu']
