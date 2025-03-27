from django import forms
from authentication.models import Buyer, Admin

import re
from django import forms
from django.core.exceptions import ValidationError
from authentication.models import Buyer, Admin

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['username', 'full_name', 'email', 'alamat', 'no_hp', 'jenis_kelamin']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'alamat': forms.TextInput(attrs={'class': 'form-control'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not re.match(r'^[A-Za-z0-9_.-]+$', username):
            raise ValidationError("Username hanya boleh berisi huruf, angka, underscore, titik, dan strip.")
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not re.match(r'^[A-Za-z\s_.-]+$', full_name):
            raise ValidationError("Nama lengkap hanya boleh berisi huruf, spasi, underscore, titik, dan strip.")
        return full_name

    def clean_alamat(self):
        alamat = self.cleaned_data.get('alamat', '').strip()
        # Izinkan huruf, angka, spasi, koma, titik, strip dan karakter aman lainnya
        if not re.match(r'^[A-Za-z0-9\s,.\-#/]+$', alamat):
            raise ValidationError("Alamat mengandung karakter yang tidak diizinkan.")
        return alamat

    def clean_no_hp(self):
        no_hp = self.cleaned_data.get('no_hp', '').strip()
        if not re.match(r'^\d+$', no_hp):
            raise ValidationError("Nomor HP harus hanya berisi angka.")
        return no_hp

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        # EmailField bawaan sudah melakukan validasi format
        return email


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['username', 'full_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not re.match(r'^[A-Za-z0-9_.-]+$', username):
            raise ValidationError("Username hanya boleh berisi huruf, angka, underscore, titik, dan strip.")
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not re.match(r'^[A-Za-z\s_.-]+$', full_name):
            raise ValidationError("Nama lengkap hanya boleh berisi huruf, spasi, underscore, titik, dan strip.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        return email
