from rest_framework import serializers
from .models import Product, ProductInventoryLog

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'category', 'price', 'quantity']


class ProductInventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryLog
        fields = '__all__'