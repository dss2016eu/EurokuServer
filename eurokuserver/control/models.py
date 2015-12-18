# -*- coding: utf-8 -*-
from django.db import models

LANGUAGES = (('es', 'Español'),
             ('eu', 'Euskara'),
             ('pl', 'Polako'))

# Create your models here.
class ControlPanel(models.Model):
    difficulty = models.SmallIntegerField()

class Device(models.Model):
    token = models.CharField(max_length=100)
    language = models.CharField(max_length=5, choices=LANGUAGES)
