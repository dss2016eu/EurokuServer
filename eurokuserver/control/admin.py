from django.contrib import admin

from .models import ControlPanel, Device

# Register your models here.
admin.site.register(ControlPanel)
admin.site.register(Device)
