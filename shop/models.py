from django.db import models
from django.utils import timezone

# -----------------------------
# Product Model
# -----------------------------
class Product(models.Model):
    """Model for vending machine products"""
    CATEGORY_CHOICES = [
        ('CAKE', 'Cakes'),
        ('DRINK', 'Soft Drinks'),
    ]
    
    # Remove product_id and let Django handle the primary key automatically
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=10)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']  # Change to 'id'
    
    def __str__(self):
        return f"{self.id} - {self.name}"  # Change to self.id
    
    @property
    def is_available(self):
        """Return True if the product is in stock"""
        return self.quantity > 0


# -----------------------------
# Transaction Model
# -----------------------------
class Transaction(models.Model):
    """Model for purchase transactions"""
    transaction_date = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    money_inserted = models.DecimalField(max_digits=10, decimal_places=2)
    change_returned = models.DecimalField(max_digits=10, decimal_places=2)
    stock_after = models.IntegerField()
    
    class Meta:
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"Transaction {self.id} - {self.product.name} x{self.quantity}"


# -----------------------------
# MoneyInserted Model
# -----------------------------
class MoneyInserted(models.Model):
    """Model for tracking money inserted per transaction"""
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='money_details')
    denomination = models.IntegerField()
    count = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Rs {self.denomination} x{self.count}"


# -----------------------------
# ChangeReturned Model
# -----------------------------
class ChangeReturned(models.Model):
    """Model for tracking change returned per transaction"""
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='change_details')
    denomination = models.IntegerField()
    count = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Rs {self.denomination} x{self.count}"