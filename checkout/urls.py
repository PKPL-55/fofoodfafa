from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('remove_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]