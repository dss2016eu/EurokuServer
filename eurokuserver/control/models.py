# -*- coding: utf-8 -*-
from django.db import models
import uuid
import datetime


LANGUAGES = (('es', 'Español'),
             ('eu', 'Euskara'),
             ('en', 'English'))

INFOPOINT_DESC_TEMPLATE = u"""\
<p>
<br/>
<b>{0}</b>
<br/>{1}
<br/>{2}</p>
"""
INFOPOINT = {'eu': INFOPOINT_DESC_TEMPLATE.format(u'2016 Gunea',
                                                  u'Easo kalea, 43 Donostia / San Sebastián, 20006',
                                                  u'Ordutegia: Astelehenetik ostiralera 09:00-19:00'),
             'es': INFOPOINT_DESC_TEMPLATE.format(u'Espacio 2016',
                                                  u'Calle Easo, 43 Donostia / San Sebastián, 20006',
                                                  u'Horario: de lunes a viernes 09:00-19:00'),
             'en': INFOPOINT_DESC_TEMPLATE.format(u'Space 2016',
                                                  u'Easo street, 43 Donostia / San Sebastián, 20006 Spain',
                                                  u'Schedule: from Monday to Friday 09:00-19:00'),
             'latlong': u'43.315329, -1.982663'}


# Create your models here.
class ControlPanel(models.Model):
    difficulty_max = models.SmallIntegerField()
    difficulty_min = models.SmallIntegerField()
    zenbat_egunez_saria = models.SmallIntegerField(default=30)
    sari_kopurua_max = models.SmallIntegerField(default=100)

    
    def get_difficulty_for_device(self, device):
        from eurokuserver.price.models import DevicePrice
        price_limit = datetime.date.today() - datetime.timedelta(self.zenbat_egunez_saria)
        price_in_period = DevicePrice.objects.filter(device=device, added__gte=price_limit)

        difficulty = self.difficulty_min
        price_count = price_in_period.count()
        if self.sari_kopurua_max > 0:
            difficulty = self.difficulty_min + (price_count * (self.difficulty_max - self.difficulty_min) / self.sari_kopurua_max)
        return difficulty

class DeviceManager(models.Manager):
    def new(self, language):
        device_token = uuid.uuid4().get_hex().replace('-', '')
        device = Device.objects.create(token=device_token,
                                       language=language)
        return device


class Device(models.Model):
    token = models.CharField(max_length=100)
    language = models.CharField(max_length=5, choices=LANGUAGES)

    objects = DeviceManager()
