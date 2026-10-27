import copy
import unittest
from datetime import datetime
from bazi_luck import calculate_bazi_luck
from dayun_reading import verified_dayun_reading

class VerifiedDaYunTests(unittest.TestCase):
    def setUp(self):
        self.birth = datetime(2005, 12, 23, 8, 37)

    def make(self, code=1, sect=1, count=5):
        return calculate_bazi_luck(
            self.birth, gender=code, yun_sect=sect,
            day_sect=2, cycles=count, timezone_verified="Asia/Yangon",
        )

    def test_both_traditional_direction_codes_and_sects(self):
        for code in (0, 1):
            for sect in (1, 2):
                with self.subTest(code=code, sect=sect):
                    result=verified_dayun_reading(self.make(code, sect))
                    self.assertEqual(len(result["periods"]),5)
                    self.assertEqual(result["rule_id"],"CHN-BAZI-DAYUN-001")
                    self.assertEqual(result["method_code"],code)
                    self.assertFalse(result["prediction_supported"])
                    self.assertEqual(result["direction"] in ("顺行","逆行"),True)

    def test_direction_reversal_when_code_changes(self):
        male=verified_dayun_reading(self.make(1))
        female=verified_dayun_reading(self.make(0))
        self.assertNotEqual(male["direction"],female["direction"])

    def test_reject_forged_period_and_matching_evidence(self):
        modified=self.make()
        modified["periods"][0]["gan_zhi"]="甲子"
        modified["evidence"]["derived_facts"]["periods"][0]["gan_zhi"]="甲子"
        with self.assertRaises(ValueError):
            verified_dayun_reading(modified)

    def test_reject_changed_birth_time(self):
        modified=self.make()
        modified["evidence"]["input_assumptions"]["birth_wall_clock"]="2006-12-23T08:37:00"
        with self.assertRaises(ValueError):
            verified_dayun_reading(modified)

    def test_reject_mismatched_method_code(self):
        modified=self.make()
        modified["evidence"]["input_assumptions"]["gender_explicit_library_convention"]=0
        with self.assertRaises(ValueError):
            verified_dayun_reading(modified)

    def test_reject_unverified_rule(self):
        modified=self.make()
        modified["evidence"]["rule_id"]="UNRESEARCHED"
        with self.assertRaises(ValueError):
            verified_dayun_reading(modified)

    def test_periods_are_ten_years_each(self):
        result=verified_dayun_reading(self.make(count=8))
        for p in result["periods"]:
            self.assertEqual(p["end_year"]-p["start_year"],9)
            self.assertEqual(p["end_age_nominal"]-p["start_age_nominal"],9)

if __name__=="__main__":
    unittest.main()
