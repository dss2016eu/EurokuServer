import datetime

from django.test import TestCase
from .models import ControlPanel, Device
from eurokuserver.game.models import Game
from eurokuserver.price.models import Price
from eurokuserver.price.utils import get_price

# Create your tests here.
class ControlTest(TestCase):
    def setUp(self):
        for p in range(100):
            Price.objects.create(title_eu='aa {} eu'.format(p),
                                 title_es='aa {} es'.format(p),
                                 title_en='aa {} en'.format(p),
                                 url_eu='aa {} eu'.format(p),
                                 url_es='aa {} es'.format(p),
                                 url_en='aa {} en'.format(p),
                                 event=False,
                                 total=100,
                                 valid_until=datetime.date.today() + datetime.timedelta(days=1),
                                 available=100,
                                 active=True)
            ControlPanel.objects.create(difficulty_max=40,
                                        difficulty_min=10)
            self.cp = ControlPanel.objects.all()[0]
            self.device = Device.objects.new(language='eu')
            
    def test_new_device_gets_minimal_difficulty(self):
        self.assertEqual(self.cp.difficulty_min,
                         self.cp.get_difficulty_for_device(self.device))
        
    def test_device_without_price_gets_minimal_difficulty(self):
        for g in range(10):
            Game.objects.create(device=self.device,
                                points_to_win=10)
        self.assertEqual(self.cp.difficulty_min,
                         self.cp.get_difficulty_for_device(self.device))
        
    def test_device_without_price_in_period_get_minimal_dififculty(self):
        p = get_price(self.device)
        days_off_period = datetime.timedelta(days=self.cp.zenbat_egunez_saria + 1)
        p.added = p.added - days_off_period
        p.save()
        self.assertEqual(self.cp.difficulty_min,
                         self.cp.get_difficulty_for_device(self.device))
