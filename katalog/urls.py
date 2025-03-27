from django.contrib import admin
from django.urls import path
from katalog.views import main_view, get_products_json, detail_product, delete_product, admin_dashboard

app_name = 'katalog'

urlpatterns = [
    path('', main_view, name='main_view'),
    path('json/', get_products_json, name='view_json'),
    path('product/<int:product_id>/', detail_product, name='detail_product'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
]