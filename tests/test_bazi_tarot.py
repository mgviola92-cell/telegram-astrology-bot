import unittest
from datetime import datetime
from tarot_core import DECK, draw_tarot
from bazi_core import calculate_bazi

class TarotTests(unittest.TestCase):
    def test_deck(self):
        self.assertEqual(len(DECK), 78)
        self.assertEqual(len(set(DECK)), 78)
    def test_draw_unique(self):
        result=draw_tarot('three')
        self.assertEqual(len(result['cards']), 3)
        self.assertEqual(len({c['card'] for c in result['cards']}),3)
        self.assertIn('rule_id',result['evidence'])
    def test_bad_spread(self):
        with self.assertRaises(ValueError): draw_tarot('seven')

class BaziTests(unittest.TestCase):
    def test_upstream_reference(self):
        try: import lunar_python
        except ImportError: self.skipTest('optional lunar-python not installed')
        p=calculate_bazi(datetime(2005,12,23,8,37))['pillars']
        self.assertEqual(p,{'year':'乙酉','month':'戊子','day':'辛巳','hour':'壬辰'})
    def test_reject_timezone_aware(self):
        from datetime import timezone
        with self.assertRaises(ValueError): calculate_bazi(datetime(2000,1,1,tzinfo=timezone.utc))
    def test_invalid_sect(self):
        with self.assertRaises(ValueError): calculate_bazi(datetime(2000,1,1),sect=3)

if __name__=='__main__': unittest.main()
