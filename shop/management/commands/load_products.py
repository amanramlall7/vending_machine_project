from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Load initial products into the database'

    def handle(self, *args, **kwargs):
        # Clear existing products
        Product.objects.all().delete()
        
        # Cakes data (with Japanese snacks)
        cakes = [
            ("Sando", 15, 10),
            ("Biscrem", 25, 10),
            ("Pocky (Strawberry)", 30, 10),  # Traditional Japanese snack
            ("Taiyaki (Red Bean)", 35, 10),  # Traditional Japanese fish-shaped cake
            ("M&Ms", 50, 10),
            ("Motto", 23, 10),
        ]
        
        # Drinks data (with Japanese drinks)
        drinks = [
            ("Ramune (Original)", 55, 10),  # Traditional Japanese marble soda
            ("Calpico (Calpis)", 50, 10),   # Traditional Japanese drink
            ("Mirinda (raspberry)", 45, 10),
            ("Water", 25, 10),
            ("Sparkling Water (Vital)", 40, 10),
            ("Coca Cola", 45, 10),
        ]
        
        # Create cake products
        for name, price, quantity in cakes:
            Product.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                category='CAKE'
            )
            self.stdout.write(self.style.SUCCESS(f'Created cake: {name}'))
        
        # Create drink products
        for name, price, quantity in drinks:
            Product.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                category='DRINK'
            )
            self.stdout.write(self.style.SUCCESS(f'Created drink: {name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded {len(cakes) + len(drinks)} products!'))