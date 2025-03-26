import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Buyer, Admin
from captcha.fields import CaptchaField


name_validator = RegexValidator(
    regex=r'^[A-Za-z0-9._-]+$',
    message="Nama hanya boleh berisi huruf, angka, dan karakter . _ -"
)


password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^\w\s]).{8,}$'

class BuyerRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=30, 
        required=True, 
        validators=[name_validator],
        label="Nama Lengkap"
    )
    email = forms.EmailField(required=True, label="Email")
    alamat = forms.CharField(max_length=255, required=True, label="Alamat")
    no_hp = forms.CharField(max_length=15, required=True, label="Nomor HP",
                            help_text="Masukkan nomor telepon dengan kode negara, tanpa '+' atau '-' (contoh: 62123456)")
    jenis_kelamin = forms.CharField(max_length=10, required=True, label="Jenis Kelamin")
    # Jika diperlukan, Anda dapat menambahkan field tanggal_lahir di sini
    captcha = CaptchaField(label="Masukkan Captcha")
    class Meta:
        model = Buyer
        fields = (
            'username', 
            'full_name', 
            'email', 
            'alamat', 
            'no_hp', 
            'jenis_kelamin', 
            'password1', 
            'password2'
        )
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not re.match(password_pattern, password1):
            raise ValidationError("Password harus minimal 8 karakter dan mengandung setidaknya satu huruf, satu angka, dan satu karakter spesial.")
        return password1
    
    def clean_no_hp(self):
        no_hp = self.cleaned_data.get('no_hp')
        # Validasi tidak mengandung '+' atau '-'
        if '+' in no_hp or '-' in no_hp:
            raise ValidationError("Nomor HP tidak boleh mengandung tanda '+' atau '-'.")
        # Pastikan hanya berisi angka
        if not no_hp.isdigit():
            raise ValidationError("Nomor HP harus hanya berisi angka.")
        # Periksa panjang minimal 8 dan maksimal 15 karakter
        if not (8 <= len(no_hp) <= 15):
            raise ValidationError("Nomor HP harus memiliki panjang antara 8 sampai 15 digit.")
        return no_hp
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Set role Buyer secara eksplisit
        user.role = 'buyer'
        if commit:
            user.save()
        return user

class AdminRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=30, 
        required=True, 
        validators=[name_validator],
        label="Nama Lengkap"
    )
    email = forms.EmailField(required=True, label="Email")
    # Jika diperlukan, tambahkan field tambahan untuk Admin

    captcha = CaptchaField(label="Masukkan Captcha")
    class Meta:
        model = Admin
        fields = ('username', 'full_name', 'email', 'password1', 'password2')
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not re.match(password_pattern, password1):
            raise ValidationError("Password harus minimal 8 karakter dan mengandung setidaknya satu huruf, satu angka, dan satu karakter spesial.")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set role Admin secara eksplisit
        user.role = 'admin'
        if commit:
            user.save()
        return user
