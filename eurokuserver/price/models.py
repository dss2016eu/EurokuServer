import datetime

from django.db import models
from django.utils import timezone

from eurokuserver.control.models import Device

# Create your models here.

class PriceManager(models.Manager):
    def get_available(self):
        return self.filter(active=True, valid_until__gte = timezone.now())

class Price(models.Model):
    title_eu = models.CharField(max_length=250)
    title_es = models.CharField(max_length=250)
    title_en = models.CharField(max_length=250)
    url_eu = models.CharField(max_length=250)
    url_es = models.CharField(max_length=250)
    url_en = models.CharField(max_length=250)
    event = models.BooleanField()
    total = models.SmallIntegerField()
    available = models.SmallIntegerField()
    valid_until = models.DateField('Noiz da ebentoa?')
    active = models.BooleanField(default=False)

    objects = PriceManager()

    def get_title(self, lang=None):
        if lang is None:
            return self.title_eu
        else:
            return getattr(self, 'title_{0}'.format(lang), self.title_eu)

    def get_url(self, lang=None):
        if lang is None:
            return self.url_eu
        else:
            return getattr(self, 'url_{0}'.format(lang), self.url_eu)
        
    def get_last_date_to_claim(self):
        if self.event:
            return self.valid_until - datetime.timedelta(days=1)
        
    def __unicode__(self):
        return self.get_title()
        
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
        return self.price.get_title()

    def device_token(self):
        return self.device.token
    
