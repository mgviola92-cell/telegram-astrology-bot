"""Independent astronomical checks from NOAA/NASA and USNO published formulas.

Reference J2000 = 2000-01-01 12:00 UTC, JD 2451545.0.
Meeus GMST at this epoch = 280.46061837 degrees.
Mean obliquity at this epoch = 23° 26′ 21.448″.
No planetary positions or empirical forecasting claims follow from these tests.
"""
import unittest
from datetime import datetime, timezone, date
from astro_core import annual_profection
from western_houses import (
    julian_day, greenwich_mean_sidereal, mean_obliquity,
    ascendant_from_sidereal, whole_sign_houses, calculate_whole_sign_chart,
)

EPOCH=datetime(2000,1,1,12,0,0,tzinfo=timezone.utc)

class WesternAstronomyBenchmarkTests(unittest.TestCase):
    def test_j2000_utc_julian_day(self):
        self.assertEqual(julian_day(EPOCH),2451545.0)

    def test_noaa_jpl_meuus_greenwich_mean_sidereal_time(self):
        self.assertAlmostEqual(greenwich_mean_sidereal(2451545.0),280.46061837,places=7)

    def test_mean_obliquity_j2000_reference(self):
        expected=23+26/60+21.448/3600
        self.assertAlmostEqual(mean_obliquity(2451545.0),expected,places=9)

    def test_ascendant_equatorial_quadrants(self):
        epsilon=mean_obliquity(2451545.0)
        for lst,expected in ((0,90),(90,180),(180,270),(270,0)):
            with self.subTest(lst=lst):
                longitude=ascendant_from_sidereal(lst,0,epsilon)
                separation=min(abs(longitude-expected),360-abs(longitude-expected))
                self.assertLess(separation,1e-8)

    def test_rising_sign_shift_with_geographic_longitude(self):
        j=calculate_whole_sign_chart(EPOCH,79.53938163,0)
        self.assertAlmostEqual(j["local_mean_sidereal_deg"],0,places=6)
        self.assertAlmostEqual(j["ascendant_longitude"],90,places=5)
        self.assertEqual(j["rising_sign"],"Cancer")

    def test_twelve_houses_follow_ascendant(self):
        houses=whole_sign_houses(87.5)
        self.assertEqual(len(houses),12)
        self.assertEqual(houses[0],{"house":1,"sign":"Gemini"})
        self.assertEqual(houses[-1],{"house":12,"sign":"Taurus"})

    def test_annual_profections_repeat_every_twelve_ages(self):
        birth=date(2000,1,1)
        for when,house,sign in ((date(2000,1,1),1,"Aries"),
                                (date(2001,1,1),2,"Taurus"),
                                (date(2012,1,1),1,"Aries"),
                                (date(2024,1,1),1,"Aries"),
                                (date(2025,1,1),2,"Taurus")):
            with self.subTest(when=when):
                x=annual_profection(birth,when,"Aries")
                self.assertEqual(x["house"],house)
                self.assertEqual(x["sign"],sign)

if __name__=="__main__":
    unittest.main()
