from django.urls import path
from .views import *

app_name = 'userprofile'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', edit_profile, name='edit_profile')
]