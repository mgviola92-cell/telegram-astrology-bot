import unittest
from datetime import date
from myanmar_calendar import calculate_myanmar_calendar, astrology_days, jdn_to_myanmar

class MyanmarCalendarTests(unittest.TestCase):
    def test_upstream_reference_january_2024(self):
        v=calculate_myanmar_calendar(date(2024,1,1))
        self.assertEqual((v['myanmar_year'],v['month'],v['day'],v['mahabote']),
                         (1385,'Nadaw',20,'Marana'))
    def test_new_year_boundary(self):
        v=calculate_myanmar_calendar(date(2024,4,17))
        self.assertEqual((v['myanmar_year'],v['month'],v['day']), (1386,'Tagu',9))
    def test_waso_full_moon(self):
        v=calculate_myanmar_calendar(date(2024,7,20))
        self.assertEqual((v['month'],v['day']),('Waso',15))
    def test_date_sequence(self):
        from datetime import timedelta
        start=date(2024,1,1)
        for n in range(366):
            d=start+timedelta(days=n)
            v=calculate_myanmar_calendar(d)
            self.assertTrue(1<=v['day']<=30)
            self.assertTrue(0<=v['month_index']<=14)
            self.assertIn(v['pyathada'],(0,1,2))
    def test_wd_algorithm(self):
        self.assertEqual(astrology_days(1,0),(False,False))
        self.assertTrue(astrology_days(1,4)[0])
    def test_reject_out_of_supported_range(self):
        with self.assertRaises(ValueError):calculate_myanmar_calendar(date(1800,1,1))
    def test_evidence(self):
        r=calculate_myanmar_calendar(date(2024,1,1))
        self.assertEqual(r['evidence']['rule_id'],'MM-CALENDAR-MMCAL-001')

if __name__ == '__main__': unittest.main()
