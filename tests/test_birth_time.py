import unittest
from datetime import datetime, timezone
from birth_time import normalize_birth_wall_time

class BirthTimezoneTests(unittest.TestCase):
    def test_yangon_historical_zone(self):
        result=normalize_birth_wall_time(datetime(2005,12,23,8,37),'Asia/Yangon')
        self.assertEqual(result['utc_offset_seconds'],23400)
        self.assertEqual(result['utc_time'],datetime(2005,12,23,2,7,tzinfo=timezone.utc))
    def test_los_angeles_summer(self):
        result=normalize_birth_wall_time(datetime(2020,7,1,12),'America/Los_Angeles')
        self.assertEqual(result['utc_offset_seconds'],-25200)
    def test_nonexistent_dst(self):
        with self.assertRaisesRegex(ValueError,'does not exist'):
            normalize_birth_wall_time(datetime(2024,3,10,2,30),'America/Los_Angeles')
    def test_ambiguous_dst(self):
        t=datetime(2024,11,3,1,30)
        with self.assertRaisesRegex(ValueError,'Ambiguous'):
            normalize_birth_wall_time(t,'America/Los_Angeles')
        a=normalize_birth_wall_time(t,'America/Los_Angeles',fold=0)
        b=normalize_birth_wall_time(t,'America/Los_Angeles',fold=1)
        self.assertEqual((b['utc_time']-a['utc_time']).total_seconds(),3600)
    def test_invalid_zone(self):
        with self.assertRaises(ValueError):
            normalize_birth_wall_time(datetime(2000,1,1),'Not_A_City')
    def test_utc_inferred_not_allowed(self):
        with self.assertRaises(ValueError):
            normalize_birth_wall_time(datetime(2000,1,1),'UTC')

if __name__=='__main__': unittest.main()
