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