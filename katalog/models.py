from django.db import models

class Product(models.Model):
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=100)  # Menambahkan kategori
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    deskripsi = models.TextField(max_length=100,blank=True, null=True)
    quantity = models.IntegerField(default=0)
    img_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nama