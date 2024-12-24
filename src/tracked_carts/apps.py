from django.apps import AppConfig


class TrackedCartsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tracked_carts"

    def ready(self):
        from . import signals
