import random
import string
import datetime

from django.conf import settings
from .models import Price, DevicePrice
from eurokuserver.control.models import ControlPanel

KEY_LENGTH = getattr(settings, 'EUROKU_PRICE_KEY_LENGTH', 8)

def _create_price_key():
    return u''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_LENGTH))
    
def get_price(device):
    # Ebenturen bat baldin bado aktibo baldin badaude
    # azkarren iraungitzen den ebentutik banatu saria
    # Ebenturik ez baldin badago, saria beste guztien
    # artean aukeratu eta randon bat egin
    day = datetime.timedelta(days=1)
    prices = Price.objects.filter(active=True, available__gt=0)
    events = prices.filter(event=True, valid_until__gte=datetime.date.today() + day).order_by('-valid_until')
    if events.exists():
        price = events.first()
    else:
        prices = prices.order_by('?')
        price = prices.first()
    price.available -= 1
    price.save()
    key = _create_price_key()
    deviceprice = DevicePrice.objects.create(device=device,
                                             price=price,
                                             key=key)
    cp = ControlPanel.objects.all()[0]
    cp.difficulty = cp.difficulty + 2
    cp.save()
    return deviceprice
