from django.urls import path
from authentication.views import *
from django.urls import path
from .views import *
from django.contrib import admin

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('refresh-captcha/', refresh_captcha, name='refresh_captcha'),
    path('validate-captcha/', validate_captcha, name='validate_captcha'),
]