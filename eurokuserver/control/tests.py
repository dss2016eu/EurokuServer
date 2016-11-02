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
        
    def test_device_under_minimal_games_count_gets_minimal_difficulty(self):
        for i in range(self.cp.partida_kopurua_min - 1):
            Game.objects.create(points_to_win=10, device=self.device)
        self.assertEqual(self.cp.difficulty_min,
                         self.cp.get_difficulty_for_device(self.device))
        
    def test_device_over_max_games_count_gets_max_difficulty(self):
        for i in range(self.cp.partida_kopurua_max + 1):
            Game.objects.create(points_to_win=10, device=self.device)
        self.assertEqual(self.cp.difficulty_max,
                         self.cp.get_difficulty_for_device(self.device))

    def test_device_over_min_games_count_gets_greater_difficulty_than_min(self):
        for i in range(self.cp.partida_kopurua_min + 1):
            Game.objects.create(points_to_win=10, device=self.device)
        self.assertGreaterEqual(self.cp.get_difficulty_for_device(self.device),
                                self.cp.difficulty_min)

    def test_device_under_max_games_count_gets_smaller_difficulty_than_max(self):
        for i in range(self.cp.partida_kopurua_max - 1):
            Game.objects.create(points_to_win=10, device=self.device)
        self.assertLessEqual(self.cp.get_difficulty_for_device(self.device),
                             self.cp.difficulty_max)

    def test_device_with_a_price_gets_max_difficulty(self):
        get_price(self.device)
        self.assertEqual(self.cp.difficulty_max,
                         self.cp.get_difficulty_for_device(self.device))

    def test_device_with_old_price_gets_min_diffyculty(self):
        dp = get_price(self.device)
        dp.added = dp.added - (datetime.timedelta(self.cp.zenbat_egunez_saria + 1))
        dp.save()
        self.assertEqual(self.cp.difficulty_min,
                         self.cp.get_difficulty_for_device(self.device))

    def test_device_gets_min_difficulty_when_max_and_min_are_equal(self):
        self.cp.difficulty_max = self.cp.difficulty_min
        self.assertEqual(self.cp.difficulty_min,
                         self.cp.get_difficulty_for_device(self.device))
        
