from django.core.management.base import BaseCommand

from ...adding_menu_script import add_menu


class Command(BaseCommand):
    help = "Add menu for restaurants"

    def handle(self, *args, **kwargs):
        add_menu()
        self.stdout.write(self.style.SUCCESS("The menu has been added successfully"))
