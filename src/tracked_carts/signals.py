from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Cart
from restaurants.models import Restaurant
from tracked_carts.models import TrackedCart


@receiver(post_save, sender=Cart)
def process_carts_and_track(sender, instance, created, **kwargs):
    restaurants = Cart.objects.filter(status=None).values_list("restaurant", flat=True).distinct()

    for restaurant_id in restaurants:
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)

            total_sum = (
                Cart.objects.filter(restaurant=restaurant, status=None).aggregate(total=Sum("total_price"))["total"]
                or 0
            )

            if total_sum > restaurant.free_shipping_price:
                carts_to_track = Cart.objects.filter(restaurant=restaurant, status=None)

                tracked_cart = TrackedCart.objects.create(status=True)
                tracked_cart.carts.add(*carts_to_track)

                carts_to_track.update(status=True)

        except Restaurant.DoesNotExist:
            continue
