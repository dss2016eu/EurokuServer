from django.db import models
from eurokuserver.control.models import Device

# Create your models here.
class Price(models.Model):
    title = models.CharField(max_length=250)
    event = models.BooleanField()
    total = models.SmallIntegerField()
    available = models.SmallIntegerField()
    valid_until = models.DateField()
    muste_claim_days_delta = models.SmallIntegerField()
    active = models.BooleanField(default=False)

class DevicePrice(models.Model):
    device = models.ForeignKey(Device)
    price = models.ForeignKey(Price)
    key = models.CharField(max_length=30)
    claimed = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    
