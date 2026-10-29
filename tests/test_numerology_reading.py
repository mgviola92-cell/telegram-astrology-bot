"""Offline checks: sourced, non-predictive Numerology Life Path interpretations."""
import unittest
from datetime import date
from astro_core import life_path
from numerology_reading import NUMBER_THEMES, RULE_ID, interpret_life_path
from personal_reading import personal_reading
from evidence_ui import get_rule

class LifePathThemeTests(unittest.TestCase):
    def test_all_twelve_conventions_are_covered(self):
        self.assertEqual(set(NUMBER_THEMES), set(range(1, 10)) | {11,22,33})
        self.assertIn("numerology.com",get_rule(RULE_ID)["source"].lower())
        for number,(title,interpretation) in NUMBER_THEMES.items():
            with self.subTest(number=number):
                self.assertTrue(title)
                self.assertGreater(len(interpretation),35)
                self.assertLess(len(interpretation),500)
    def test_explicit_arithmetic_stays_separate_from_traditional_meaning(self):
        for day in (date(1990,5,14),date(2005,12,23),date(2024,1,3)):
            with self.subTest(day=day):
                result=life_path(day)
                desc=interpret_life_path(result)
                self.assertEqual(desc["number"],result["number"])
                self.assertEqual(desc["calculation_rule_id"],result["evidence"]["rule_id"])
                self.assertEqual(desc["interpretation_rule_id"],RULE_ID)
                self.assertFalse(desc["prediction_supported"])
                self.assertFalse(personal_reading(day)["profile_saved"])
    def test_modified_evidence_rejected(self):
        item=life_path(date(2005,12,23))
        item["number"]=8 if item["number"]!=8 else 9
        with self.assertRaises(ValueError):
            interpret_life_path(item)
        item=life_path(date(2005,12,23))
        item["evidence"]["input_assumptions"]["birth_date"]="2006-12-23"
        with self.assertRaises(ValueError):
            interpret_life_path(item)

if __name__=="__main__":
    unittest.main()
