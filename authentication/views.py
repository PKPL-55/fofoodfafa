from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import BuyerRegistrationForm, AdminRegistrationForm
from django.http import JsonResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'buyer':
            form = BuyerRegistrationForm(request.POST)
        else:
            form = AdminRegistrationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrasi berhasil!")
            return redirect('authentication:login') 
        else:
            messages.error(request, "Terjadi kesalahan saat registrasi. Silakan periksa data yang Anda masukkan.")
    else:
        # Menampilkan form default (misalnya, AdminRegistrationForm) untuk inisialisasi
        form = AdminRegistrationForm()
    return render(request, 'register_page.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            print(form)
            messages.success(request, "Login berhasil!")
            return redirect('main:show_main')
        else:
            messages.error(request, "Login gagal, periksa kembali username dan password Anda.")
    else:
        form = AuthenticationForm()
    return render(request, 'login_page.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Anda telah berhasil logout.")
    return redirect('authentication:login')

def refresh_captcha(request):
    new_key = CaptchaStore.generate_key()
    new_image_url = captcha_image_url(new_key)
    data = {
        'key': new_key,
        'image_url': new_image_url,
    }
    return JsonResponse(data)

def validate_captcha(request):
    key = request.GET.get('key')
    response = request.GET.get('response')
    valid = False
    try:
        captcha_obj = CaptchaStore.objects.get(hashkey=key)
        if response.strip().lower() == captcha_obj.response.strip().lower():
            valid = True
    except CaptchaStore.DoesNotExist:
        valid = False
    return JsonResponse({'valid': valid})
