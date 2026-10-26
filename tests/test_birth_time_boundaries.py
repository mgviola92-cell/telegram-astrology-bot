import unittest
from datetime import datetime,timezone,timedelta
from birth_time import normalize_birth_wall_time

class BirthTimeBoundariesTests(unittest.TestCase):
    def test_yangon_wall_clock_to_utc(self):
        result=normalize_birth_wall_time(datetime(2005,12,23,8,37),"Asia/Yangon")
        self.assertEqual(result["utc_offset_seconds"],23400)
        self.assertEqual(result["utc_time"],datetime(2005,12,23,2,7,tzinfo=timezone.utc))
        self.assertFalse(result["true_solar_time_applied"])

    def test_reject_utc_zone_as_birth_location(self):
        with self.assertRaises(ValueError):
            normalize_birth_wall_time(datetime(2005,12,23,8,37),"UTC")

    def test_reject_aware_wall_clock(self):
        with self.assertRaises(ValueError):
            normalize_birth_wall_time(datetime(2005,12,23,8,37,tzinfo=timezone.utc),"Asia/Yangon")

    def test_new_york_spring_gap(self):
        with self.assertRaises(ValueError):
            normalize_birth_wall_time(datetime(2024,3,10,2,30),"America/New_York")

    def test_new_york_fall_overlap_requires_explicit_fold(self):
        birth=datetime(2024,11,3,1,30)
        with self.assertRaises(ValueError):
            normalize_birth_wall_time(birth,"America/New_York")
        early=normalize_birth_wall_time(birth,"America/New_York",fold=0)
        late=normalize_birth_wall_time(birth,"America/New_York",fold=1)
        self.assertEqual(late["utc_time"]-early["utc_time"],timedelta(hours=1))
        self.assertTrue(early["dst_ambiguous"])
        self.assertTrue(late["dst_ambiguous"])

    def test_invalid_fold(self):
        with self.assertRaises(ValueError):
            normalize_birth_wall_time(datetime(2024,11,3,1,30),"America/New_York",fold=2)

if __name__=="__main__":
    unittest.main()
