import random
import string

from django.conf import settings
from .models import Price, DevicePrice

KEY_LENGTH = getattr(settings, 'EUROKU_PRICE_KEY_LENGTH', 8)

def _create_price_key():
    return u''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_LENGTH))
    
def get_price(device):
    # Ebenturen bat baldin bado aktibo baldin badaude
    # azkarren iraungitzen den ebentutik banatu saria
    # Ebenturik ez baldin badago, saria beste guztien
    # artean aukeratu eta randon bat egin
    prices = Price.objects.filter(active=True, available__gt=0)
    events = prices.filter(event=True).order_by('-valid_until')
    if events.exists():
        price = events.first()
    else:
        price = prices.first()
    price.available -= 1
    price.save()
    key = _create_price_key()
    deviceprice = DevicePrice.objects.create(device=device,
                                             price=price,
                                             key=key)
    return deviceprice