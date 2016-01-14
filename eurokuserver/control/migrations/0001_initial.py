# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ControlPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('language', models.CharField(choices=[(b'es', b'Espa\xc3\xb1ol'), (b'eu', b'Euskara'), (b'pl', b'Polako')], max_length=5)),
            ],
        ),
    ]