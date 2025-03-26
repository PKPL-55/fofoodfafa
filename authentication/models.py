import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=5, choices=ROLES, default='buyer')
    full_name = models.CharField(max_length=30)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def is_admin(self):
        return self.role == 'admin'

    def is_buyer(self):
        return self.role == 'buyer'

    def __str__(self):
        return self.username


class Buyer(User):
    alamat = models.CharField(max_length=255)
    saldo = models.IntegerField(default=0)
    no_hp = models.CharField(max_length=14)
    jenis_kelamin = models.CharField(max_length=10)
    # Jika diperlukan override, email bisa disertakan ulang, namun AbstractUser sudah menyediakan field email.
    # email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyers'


class Admin(User):
    # Tidak ada atribut baru; cukup mewarisi dari User.
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
