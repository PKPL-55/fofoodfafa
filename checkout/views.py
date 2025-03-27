from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Cart
from katalog.models import Product

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'view_cart.html', context)

@login_required
@require_POST
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))

        # Validasi stok
        if quantity > product.quantity:
            return JsonResponse({
                'success': False, 
                'error': 'Jumlah melebihi stok yang tersedia'
            })

        # Cek apakah produk sudah ada di cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Jika item sudah ada, update jumlahnya
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({'success': True})
    
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'error': 'Produk tidak ditemukan'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        })

@login_required
@require_POST
def update_cart(request, cart_item_id):
    data = json.loads(request.body)
    new_quantity = data.get('quantity')
    
    try:
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.quantity = new_quantity
        cart_item.save()
        return JsonResponse({'success': True})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart item not found'})

@login_required
@require_POST
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        return JsonResponse({'success': True})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart item not found'})
