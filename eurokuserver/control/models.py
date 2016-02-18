# -*- coding: utf-8 -*-
from django.db import models
import uuid

LANGUAGES = (('es', 'Español'),
             ('eu', 'Euskara'),
             ('en', 'English'))

# Create your models here.
class ControlPanel(models.Model):
    difficulty = models.SmallIntegerField()

class DeviceManager(models.Manager):
    def new(self, language):
        device_token = uuid.uuid4().get_hex().replace('-','')
        device = Device.objects.create(token=device_token,
                                       language=language)
        return device
    
class Device(models.Model):
    token = models.CharField(max_length=100)
    language = models.CharField(max_length=5, choices=LANGUAGES)

    objects = DeviceManager()
