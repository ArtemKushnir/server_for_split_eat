from django.core.management.base import BaseCommand

from ...adding_restaurants import add_restaurants


class Command(BaseCommand):
    help = "Add restaurants to the database"

    def handle(self, *args, **kwargs):
        add_restaurants()
        self.stdout.write(self.style.SUCCESS("Restaurants added successfully!"))
