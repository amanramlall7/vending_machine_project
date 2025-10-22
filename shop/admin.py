from django.contrib import admin
from .models import Product, Transaction, MoneyInserted, ChangeReturned

# -----------------------------
# Inline Models for Transaction
# -----------------------------
class MoneyInsertedInline(admin.TabularInline):
    model = MoneyInserted
    extra = 0
    # Use actual fields from MoneyInserted model
    readonly_fields = ('denomination', 'count')


class ChangeReturnedInline(admin.TabularInline):
    model = ChangeReturned
    extra = 0
    # Use actual fields from ChangeReturned model
    readonly_fields = ('denomination', 'count')


# -----------------------------
# Product Admin
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category', 'is_available_display')
    # list_filter must refer to actual model fields
    list_filter = ('category',)
    search_fields = ('name', 'id')
    list_editable = ('price', 'quantity')
    ordering = ('category', 'name')
    list_per_page = 20
    fieldsets = (
        ("Product Details", {
            'fields': ('id', 'name', 'category', 'price', 'quantity', 'image')
        }),
    )

    # Display available status as boolean (derived from quantity)
    def is_available_display(self, obj):
        return obj.quantity > 0
    is_available_display.boolean = True
    is_available_display.short_description = 'Available'


# -----------------------------
# Transaction Admin
# -----------------------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'transaction_date', 
        'product', 
        'quantity', 
        'total_price', 
        'money_inserted', 
        'change_returned', 
        'stock_after'
    )
    list_filter = ('transaction_date', 'product')
    search_fields = ('product__name',)
    readonly_fields = (
        'transaction_date', 
        'product', 
        'quantity', 
        'total_price', 
        'money_inserted', 
        'change_returned', 
        'stock_after'
    )
    inlines = [MoneyInsertedInline, ChangeReturnedInline]

    def has_add_permission(self, request):
        # Prevent adding transactions manually (they are system-generated)
        return False


# -----------------------------
# Customize admin site appearance
# -----------------------------
admin.site.site_header = "Vending Machine Administration"
admin.site.site_title = "Vending Machine Admin"
admin.site.index_title = "Welcome to the Vending Machine Control Panel"
