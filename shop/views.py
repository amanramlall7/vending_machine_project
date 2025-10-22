from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction as db_transaction
from .models import Product, Transaction, MoneyInserted, ChangeReturned
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from decimal import Decimal

VALID_DENOMINATIONS = [1, 5, 10, 20, 25, 50, 100]

# Landing page
def home(request):
    return render(request, 'shop/home.html')

# Vending machine page
def vending_machine(request):
    products = Product.objects.all()
    cakes = products.filter(category__iexact='CAKE')
    drinks = products.filter(category__iexact='DRINK')
    
    context = {
        'cakes': cakes,
        'drinks': drinks,
        'valid_denominations': VALID_DENOMINATIONS,
    }
    return render(request, 'shop/vending.html', context)

# Calculate change breakdown
def calculate_change(amount):
    change_breakdown = []
    remaining = int(amount)
    
    for denom in sorted(VALID_DENOMINATIONS, reverse=True):
        if remaining >= denom:
            count = remaining // denom
            change_breakdown.append({'denomination': denom, 'count': count})
            remaining -= denom * count
    
    return change_breakdown

# Handle purchase
def process_purchase(request):
    if request.method == 'POST':
        try:
            product_id = int(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity'))
            money_inserted = Decimal(request.POST.get('money_inserted'))
            
            # Validate denomination
            if int(money_inserted) not in VALID_DENOMINATIONS:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid denomination. Use: 1, 5, 10, 20, 25, 50, or 100'
                })
            
            # Get product
            product = get_object_or_404(Product, id=product_id)  # Change to id
            
            # Validate quantity
            if quantity <= 0:
                return JsonResponse({'success': False, 'message': 'Quantity must be greater than 0'})
            if quantity > product.quantity:
                return JsonResponse({'success': False, 'message': f'Not enough stock. Only {product.quantity} left'})
            
            # Calculate total
            total_price = product.price * quantity
            
            if money_inserted < total_price:
                return JsonResponse({'success': False, 'message': f'Insufficient funds. Need Rs {total_price}'})
            
            change = money_inserted - total_price
            change_breakdown = calculate_change(change)
            
            # Save transaction safely
            with db_transaction.atomic():
                product.quantity -= quantity
                product.save()
                
                trans = Transaction.objects.create(
                    product=product,
                    quantity=quantity,
                    total_price=total_price,
                    money_inserted=money_inserted,
                    change_returned=change,
                    stock_after=product.quantity
                )
                
                MoneyInserted.objects.create(transaction=trans, denomination=int(money_inserted), count=1)
                
                for item in change_breakdown:
                    ChangeReturned.objects.create(transaction=trans, denomination=item['denomination'], count=item['count'])
            
            return JsonResponse({
                'success': True,
                'message': f'Purchase successful! Bought {quantity} {product.name}',
                'change': float(change),
                'change_breakdown': change_breakdown,
                'stock_left': product.quantity
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# Purchase history
def purchase_history(request):
    transactions = Transaction.objects.all().order_by('-id')[:50]
    return render(request, 'shop/purchase_history.html', {'transactions': transactions})

# Admin panel
@staff_member_required
def admin_panel(request):
    products = Product.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)  # Change to id
        
        try:
            if action == 'update_stock':
                new_quantity = int(request.POST.get('quantity'))
                if new_quantity < 0:
                    messages.error(request, 'Quantity cannot be negative.')
                else:
                    product.quantity = new_quantity
                    product.save()
                    messages.success(request, f'Stock updated for {product.name}')
            
            elif action == 'update_price':
                new_price = Decimal(request.POST.get('price'))
                if new_price < 0:
                    messages.error(request, 'Price cannot be negative.')
                else:
                    product.price = new_price
                    product.save()
                    messages.success(request, f'Price updated for {product.name}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return redirect('admin_panel')
    
    return render(request, 'shop/admin_panel.html', {'products': products})

# Add new product
@staff_member_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if not name or not price or not quantity:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('admin_panel')

        try:
            price = Decimal(price)
            quantity = int(quantity)
            if price < 0 or quantity < 0:
                messages.error(request, 'Price and quantity cannot be negative.')
                return redirect('admin_panel')

            Product.objects.create(
                name=name,
                price=price,
                quantity=quantity,
                category=category,
                image=image
            )
            messages.success(request, f'Product "{name}" added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')

    return redirect('admin_panel')

# Update product
@staff_member_required
def update_product(request, id):  # Keep as id
    if request.method == "POST":
        try:
            product = get_object_or_404(Product, id=id)  # Keep as id
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')
            
            if price:
                product.price = Decimal(price)
            if quantity:
                product.quantity = int(quantity)
                
            product.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    return redirect('admin_panel')

# Delete product
@staff_member_required
def delete_product(request, id):  # Keep as id
    product = get_object_or_404(Product, id=id)  # Keep as id
    try:
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting product: {str(e)}')
    return redirect('admin_panel')

# Admin login
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            if user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_panel')
            else:
                messages.error(request, 'You need staff privileges to access the admin panel.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'shop/login.html')

# Admin logout
def admin_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')