from django.db import models
from django.utils import timezone

from eurokuserver.control.models import Device

# Create your models here.

class PriceManager(models.Manager):
    def get_available(self):
        return self.filter(active=True, valid_until__gte = timezone.now())

class Price(models.Model):
    title = models.CharField(max_length=250)
    event = models.BooleanField()
    total = models.SmallIntegerField()
    available = models.SmallIntegerField()
    valid_until = models.DateField()
    muste_claim_days_delta = models.SmallIntegerField()
    active = models.BooleanField(default=False)

    objects = PriceManager()

    def __unicode__(self):
        return self.title
        
class DevicePrice(models.Model):
    device = models.ForeignKey(Device)
    price = models.ForeignKey(Price)
    key = models.CharField(max_length=30)
    claimed = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)

    #####
    # used in admin site
    #####
    def price_title(self):
        return self.price.title

    def device_token(self):
        return self.device.token
    
