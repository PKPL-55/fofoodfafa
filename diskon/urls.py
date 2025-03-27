from django.urls import path
from .views import create_voucher

app_name = 'diskon'

urlpatterns = [
    path('create_voucher/', create_voucher, name='create_voucher'),
]
