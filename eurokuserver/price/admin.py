from django.contrib import admin
from .models import Price, DevicePrice

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    date_hierarchy = "valid_until"
    list_display = ('title_eu', 'event', 'total', 'available', 'valid_until', 'active')

@admin.register(DevicePrice)
class DevicePriceAdmin(admin.ModelAdmin):
    date_hierarchy = "added"
    list_display = ('device_token', 'price_title', 'claimed', 'added')


