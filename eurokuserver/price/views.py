from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import DevicePrice

@login_required
def search(request):
    claim_checkbox = False
    if request.method == 'POST':
        claim_checkbox = True
        claim = request.POST.get('claim')
        price_key = request.POST.get('key')
        dp = DevicePrice.objects.filter(key=price_key, claimed=False)
        if dp.exists():
            dp = dp.first()
            price = dp.price
            view_message = 'SARIA: {0}'.format(price.title_eu)
            if claim == u'on':
                dp.claimed = True
                dp.save()
                view_message = 'Sari esleipena ondo bukatu da'
                claim_checkbox = False
                price_key = None
        else:
            alert_message = "Gako horri dagokion banatu gabeko saririk ez dago"
            claim_checkbox = False
    return render(request, 'sariak.html', context=locals())
