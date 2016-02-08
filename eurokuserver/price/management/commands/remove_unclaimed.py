import datetime

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.utils.timezone import now

from eurokuserver.price.models import DevicePrice

class Command(NoArgsCommand):

    def handle(self, *args, **options):
        max_days_to_claim = datetime.timedelta(days=getattr(settings, 'EUROKU_MAX_DAYS_TO_CLAIM', 10))
        
        dps = DevicePrice.objects.filter(claimed=False)
        for dp in dps:
            if now() > dp.added + max_days_to_claim:
                dp.price.available += 1
                dp.price.save()
                dp.delete()
