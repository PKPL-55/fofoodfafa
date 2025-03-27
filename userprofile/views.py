# userprofile/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import User, Buyer, Admin
from .forms import BuyerProfileForm, AdminProfileForm

@login_required
def profile_view(request):
    user = request.user
    context = {'user': user}
    # Jika user adalah buyer, ambil data Buyer yang terkait
    if user.role == 'buyer':
        try:
            buyer = Buyer.objects.get(pk=user.pk)
            context['buyer'] = buyer
        except Buyer.DoesNotExist:
            context['buyer'] = None
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    if user.role == 'buyer':
        # Ambil instance Buyer secara eksplisit
        buyer_instance = Buyer.objects.get(pk=user.pk)
        form_class = BuyerProfileForm
        instance = buyer_instance
    else:
        form_class = AdminProfileForm
        instance = user

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil berhasil diperbarui!")
            return redirect('userprofile:profile')
        else:
            messages.error(request, "Terjadi kesalahan, silakan periksa kembali data Anda.")
    else:
        form = form_class(instance=instance)
    return render(request, 'edit_profile_page.html', {'form': form})
