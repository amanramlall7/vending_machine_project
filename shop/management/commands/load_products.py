from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Load initial products into the database'

    def handle(self, *args, **kwargs):
        # Clear existing products
        Product.objects.all().delete()
        
        # Cakes data (with Japanese snacks)
        cakes = [
            (41, "Sando", 15, 10),
            (42, "Biscrem", 25, 10),
            (43, "Pocky (Strawberry)", 30, 10),  # Traditional Japanese snack
            (44, "Taiyaki (Red Bean)", 35, 10),  # Traditional Japanese fish-shaped cake
            (45, "M&Ms", 50, 10),
            (46, "Motto", 23, 10),
        ]
        
        # Drinks data (with Japanese drinks)
        drinks = [
            (51, "Ramune (Original)", 55, 10),  # Traditional Japanese marble soda
            (52, "Calpico (Calpis)", 50, 10),   # Traditional Japanese drink
            (53, "Mirinda (raspberry)", 45, 10),
            (54, "Water", 25, 10),
            (55, "Sparkling Water (Vital)", 40, 10),
            (56, "Coca Cola", 45, 10),
        ]
        
        # Create cake products
        for product_id, name, price, quantity in cakes:
            Product.objects.create(
                product_id=product_id,
                name=name,
                price=price,
                quantity=quantity,
                category='CAKE'
            )
            self.stdout.write(self.style.SUCCESS(f'Created cake: {name}'))
        
        # Create drink products
        for product_id, name, price, quantity in drinks:
            Product.objects.create(
                product_id=product_id,
                name=name,
                price=price,
                quantity=quantity,
                category='DRINK'
            )
            self.stdout.write(self.style.SUCCESS(f'Created drink: {name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded {len(cakes) + len(drinks)} products!'))