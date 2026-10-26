import unittest
from datetime import datetime,timezone
from bazi_luck import calculate_bazi_luck

class DaYunTests(unittest.TestCase):
    def setUp(self):
        self.birth=datetime(2005,12,23,8,37)
    def test_gender_required(self):
        with self.assertRaises(ValueError):
            calculate_bazi_luck(self.birth,gender=2)
    def test_boolean_gender_not_accepted(self):
        with self.assertRaises(ValueError):
            calculate_bazi_luck(self.birth,gender=True)
    def test_aware_datetime_rejected(self):
        with self.assertRaises(ValueError):
            calculate_bazi_luck(datetime(2005,12,23,tzinfo=timezone.utc),gender=1)
    def test_invalid_sect(self):
        with self.assertRaises(ValueError):
            calculate_bazi_luck(self.birth,gender=1,yun_sect=3)
    def test_invalid_cycles(self):
        with self.assertRaises(ValueError):
            calculate_bazi_luck(self.birth,gender=1,cycles=0)
    def test_upstream_decade_sequence(self):
        try:import lunar_python
        except ImportError:self.skipTest("lunar-python dependency not present")
        from lunar_python import Solar
        solar=Solar.fromYmdHms(2005,12,23,8,37,0)
        upstream=solar.getLunar().getEightChar().getYun(1,1)
        got=calculate_bazi_luck(self.birth,gender=1,cycles=4,timezone_verified="Asia/Yangon")
        expected=upstream.getDaYun(5)[1:]
        self.assertEqual([p["gan_zhi"] for p in got["periods"]],[p.getGanZhi() for p in expected])
        self.assertEqual(got["forward"],upstream.isForward())
        self.assertEqual(got["start_offset"]["years"],upstream.getStartYear())
        self.assertEqual(got["evidence"]["input_assumptions"]["birth_place_timezone"],"Asia/Yangon")
    def test_opposite_gender_codes_reverse_direction(self):
        try:import lunar_python
        except ImportError:self.skipTest("lunar-python dependency not present")
        a=calculate_bazi_luck(self.birth,gender=0,cycles=2)
        b=calculate_bazi_luck(self.birth,gender=1,cycles=2)
        self.assertNotEqual(a["forward"],b["forward"])
        self.assertNotEqual([x["gan_zhi"] for x in a["periods"]],
                            [x["gan_zhi"] for x in b["periods"]])
    def test_decade_year_ranges(self):
        try:import lunar_python
        except ImportError:self.skipTest("lunar-python dependency not present")
        result=calculate_bazi_luck(self.birth,gender=1,cycles=8)
        self.assertEqual(len(result["periods"]),8)
        for previous,current in zip(result["periods"],result["periods"][1:]):
            self.assertEqual(current["start_year"],previous["end_year"]+1)
    def test_sect_2_matches_upstream(self):
        try:import lunar_python
        except ImportError:self.skipTest("lunar-python dependency not present")
        from lunar_python import Solar
        eight=Solar.fromYmdHms(2005,12,23,8,37,0).getLunar().getEightChar()
        expected=eight.getYun(0,2)
        got=calculate_bazi_luck(self.birth,gender=0,yun_sect=2,cycles=2)
        self.assertEqual(got["start_offset"]["hours"],expected.getStartHour())
        self.assertEqual(got["forward"],expected.isForward())
if __name__=="__main__":unittest.main()
