from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse

from .models import Product

def main_view(request):
    """
    Main view to display all products
    """
    products = serializers.serialize('python', Product.objects.all())
    
    context = {
        'products': products
    }
    return render(request, 'product_list.html', context)

def get_products_json(request):
    """
    API endpoint to return products as JSON
    """
    products = serializers.serialize('json', Product.objects.all())
    return JsonResponse({'products': products})

def detail_product(request, product_id):
    """
    Detailed view for a single product
    """
    # Using get_object_or_404 to automatically handle case when product doesn't exist
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product
    }
    return render(request, 'detail_product.html', context)

@login_required
def admin_dashboard(request):
    """
    View for admin dashboard to manage products
    Requires user to be logged in
    """
    # Cek apakah ada parameter edit
    edit_product = None
    if request.GET.get('edit'):
        edit_product = get_object_or_404(Product, id=request.GET.get('edit'))
    
    # Proses form tambah/edit produk
    if request.method == 'POST':
        # Cek apakah ini update atau create
        product_id = request.GET.get('edit')
        if product_id:
            # Update produk yang ada
            product = get_object_or_404(Product, id=product_id)
            product.nama = request.POST['nama']
            product.kategori = request.POST['kategori']
            product.harga = request.POST['harga']
            product.quantity = request.POST['quantity']
            product.deskripsi = request.POST['deskripsi']
            product.img_link = request.POST['img_link']
            product.save()
            messages.success(request, f'Produk {product.nama} berhasil diupdate!')
        else:
            # Buat produk baru
            product = Product.objects.create(
                nama=request.POST['nama'],
                kategori=request.POST['kategori'],
                harga=request.POST['harga'],
                quantity=request.POST['quantity'],
                deskripsi=request.POST['deskripsi'],
                img_link=request.POST['img_link']
            )
            messages.success(request, f'Produk {product.nama} berhasil ditambahkan!')
        
        return redirect('produk:admin_dashboard')

    # Ambil semua produk
    products = Product.objects.all()
    
    context = {
        'products': products,
        'edit_product': edit_product
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def delete_product(request, product_id):
    """
    View for deleting a product
    Requires user to be logged in
    """
    # Get the product or return 404
    product = get_object_or_404(Product, id=product_id)
    
    product_name = product.nama
    product.delete()
    messages.success(request, f'Produk {product_name} berhasil dihapus!')
    return redirect('produk:admin_dashboard')