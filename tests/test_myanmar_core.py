import unittest
from datetime import datetime, timezone
from myanmar_core import myanmar_birth_day

class MyanmarDayTests(unittest.TestCase):
    def test_wednesday_morning(self):
        r=myanmar_birth_day(datetime(2024,1,3,11,59))
        self.assertEqual(r['planetary_association'],'Mercury')
        self.assertIn('MM-8DAY-WEEKDAY',r['evidence']['rule_id'])
    def test_wednesday_noon(self):
        self.assertEqual(myanmar_birth_day(datetime(2024,1,3,12,0))['planetary_association'],'Rahu')
    def test_all_other_days(self):
        expected=['Moon','Mars','Jupiter','Venus','Saturn','Sun']
        for i,planet in enumerate(expected):
            # Mon Tue Thu Fri Sat Sun Jan 1,2,4,5,6,7 in 2024
            day=[1,2,4,5,6,7][i]
            with self.subTest(day=day):
                self.assertEqual(myanmar_birth_day(datetime(2024,1,day,8,0))['planetary_association'],planet)
    def test_aware_rejected(self):
        with self.assertRaises(ValueError):
            myanmar_birth_day(datetime(2024,1,3,tzinfo=timezone.utc))

if __name__ == '__main__': unittest.main()
