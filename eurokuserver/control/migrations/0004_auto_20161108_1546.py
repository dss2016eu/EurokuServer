# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-08 15:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_auto_20161024_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='controlpanel',
            old_name='partida_kopurua_max',
            new_name='sari_kopurua_max',
        ),
        migrations.RemoveField(
            model_name='controlpanel',
            name='partida_kopurua_min',
        ),
        migrations.RemoveField(
            model_name='controlpanel',
            name='zenbat_egunez_partidak',
        ),
    ]
