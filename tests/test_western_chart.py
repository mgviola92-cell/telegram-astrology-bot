import unittest
from datetime import datetime, timezone
from western_chart import tropical_sign, chart_from_longitudes, geocentric_chart

class WesternChartTests(unittest.TestCase):
    def test_all_sign_boundaries(self):
        expected=('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra',
                  'Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')
        for i,sign in enumerate(expected):
            with self.subTest(sign=sign):
                self.assertEqual(tropical_sign(i*30)['sign'], sign)
                self.assertEqual(tropical_sign(i*30)['degree_in_sign'],0)
    def test_last_fraction(self):
        self.assertEqual(tropical_sign(359.999)['sign'],'Pisces')
    def test_360_rejected(self):
        with self.assertRaises(ValueError): tropical_sign(360)
    def test_source_required(self):
        with self.assertRaises(ValueError): chart_from_longitudes({'Sun':0},verified_source='')
    def test_chart_aspects(self):
        result=chart_from_longitudes({'Sun':359,'Moon':1},verified_source='test fixture')
        self.assertEqual(result['points']['Sun']['sign'],'Pisces')
        self.assertEqual(result['aspects'][0]['aspect'],'conjunction')
        self.assertFalse(result['evidence']['input_assumptions']['birth_time_and_ephemeris_verified_by_caller'])
    def test_missing_ephemeris(self):
        with self.assertRaises(FileNotFoundError):
            geocentric_chart(datetime(2000,1,1,tzinfo=timezone.utc),'/does/not/exist.bsp')
    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):geocentric_chart(datetime(2000,1,1),'/does/not/exist.bsp')

if __name__=='__main__':unittest.main()
