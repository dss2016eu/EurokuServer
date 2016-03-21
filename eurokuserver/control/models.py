# -*- coding: utf-8 -*-
from django.db import models
import uuid

LANGUAGES = (('es', 'Español'),
             ('eu', 'Euskara'),
             ('en', 'English'))

INFOPOINT_DESC_TEMPLATE = u"""\
<p>
<br/>
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
    difficulty = models.SmallIntegerField()


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
