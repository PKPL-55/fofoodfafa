from datetime import datetime
from django.utils import timezone
import pytz
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Voucher

@login_required
def create_voucher(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_percentage = request.POST.get('discount_percentage')
        valid_until_str = request.POST.get('valid_until')

        jakarta_tz = pytz.timezone('Asia/Jakarta')

        valid_from = timezone.now().astimezone(jakarta_tz)
        valid_until_naive = datetime.strptime(valid_until_str, "%Y-%m-%dT%H:%M")
        valid_until = jakarta_tz.localize(valid_until_naive)

        Voucher.objects.create(
            code=code,
            discount_percentage=discount_percentage,
            valid_from=valid_from,
            valid_until=valid_until,
            active=True  # Selalu aktif otomatis
        )
        return redirect('diskon:create_voucher')

    now = timezone.now()
    active_vouchers = Voucher.objects.filter(
        active=True, valid_from__lte=now, valid_until__gte=now
    )

    return render(request, 'create_voucher.html', {
        'active_vouchers': active_vouchers
    })
