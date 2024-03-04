from django.core.management import BaseCommand
from shopapp.models import Product
from typing import Sequence
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")
        usery = User.objects.values_list("username", flat=True)
        print(list(usery))
        for i in usery:
            print(i)
        products_values = Product.objects.values("pk", "name")
        for p_values in products_values:
            print(p_values)
        self.stdout.write(f"Done")
