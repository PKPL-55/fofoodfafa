from django.db import models
from django.conf import settings
from katalog.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self):
        return self.product.harga * self.quantity
    
    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.nama}"
    
    class Meta:
        unique_together = ('user', 'product')  # Ensure no duplicate products in cart

class Order(models.Model):
    STATUS_CHOICES = [
        ('Dikonfirmasi', 'Dikonfirmasi'),
        ('Selesai', 'Selesai')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(Cart, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Dikonfirmasi')
    
    # Placeholder for future implementation
    discount = models.JSONField(null=True, blank=True)
    payment = models.JSONField(null=True, blank=True)

    def get_total_price(self):
        # Skeleton method to calculate total price
        return

    def __str__(self):
        return f"Order for {self.user.username} - {self.status}"