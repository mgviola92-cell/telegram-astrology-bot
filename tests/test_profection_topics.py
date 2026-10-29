"""Profection House source validation, 12-year rotation and no birth leaks."""
import copy
import unittest
from datetime import date
from astro_core import SIGNS,TRADITIONAL_RULERS
from profection_reading import profection_reading
from profection_topics import (TOPIC_RULE_ID,HOUSE_THEMES,interpret_profection,
                              render_profection_report,profection_house_glossary)

class ProfectionTopicTests(unittest.TestCase):
    def test_all_twelve_houses_and_all_rising_signs(self):
        self.assertEqual(set(HOUSE_THEMES),set(range(1,13)))
        for ascending in SIGNS:
            for age in range(24):
                with self.subTest(ascending=ascending,age=age):
                    chart=profection_reading(date(2000,1,1),date(2000+age,1,1),ascending)
                    reading=interpret_profection(chart)
                    self.assertEqual(reading["house"],age%12+1)
                    self.assertEqual(reading["next_house"],(age+1)%12+1)
                    self.assertEqual(reading["traditional_ruler"],chart["lord_of_year"])
                    self.assertEqual(reading["next_traditional_ruler"],TRADITIONAL_RULERS[SIGNS.index(reading["next_sign"])])
                    self.assertEqual(reading["interpretation_rule_id"],TOPIC_RULE_ID)
                    self.assertFalse(reading["prediction_supported"])
                    self.assertFalse(reading["transits_checked"])
                    self.assertTrue(reading["rising_sign_not_computed"])
                    self.assertTrue(reading["topic_title"])
                    self.assertTrue(reading["interpretation"])

    def test_real_birthday_boundary_and_ruler(self):
        before=profection_reading(date(2005,12,23),date(2026,12,22),"Aries")
        after=profection_reading(date(2005,12,23),date(2026,12,23),"Aries")
        self.assertEqual(interpret_profection(before)["house"],9)
        self.assertEqual(interpret_profection(after)["house"],10)
        text=render_profection_report(after,interpret_profection(after))
        self.assertIn("နှစ်တိုင်အိမ် — <b>10</b>",text)
        self.assertIn("Capricorn",text)
        self.assertIn("Saturn",text)
        self.assertIn("နောက်တစ်ဆင့်",text)
        self.assertIn("Natal ဂြိုဟ်တည်နေရာ",text)
        self.assertIn("မသိမ်း",text)
        self.assertLess(len(text),4096)
        self.assertNotIn("2005-12-23",text)
        self.assertNotIn("\\n",text)

    def test_calc_tampering_fails_closed(self):
        valid=profection_reading(date(2005,12,23),date(2026,12,23),"Aries")
        for kind in ("house","sign","lord","source_date","source_sign","evidence","derived","rising_checked"):
            bogus=copy.deepcopy(valid)
            if kind=="house":bogus["house"]=8
            elif kind=="sign":bogus["sign"]="Leo"
            elif kind=="lord":bogus["lord_of_year"]="Mars"
            elif kind=="source_date":bogus["evidence"]["input_assumptions"]["birth_date"]="2005-12-22"
            elif kind=="source_sign":bogus["evidence"]["input_assumptions"]["ascendant_sign"]="Virgo"
            elif kind=="evidence":bogus["evidence"]["rule_id"]="FAKE"
            elif kind=="derived":bogus["evidence"]["derived_facts"]["age"]=99
            else:bogus["evidence"]["input_assumptions"]["ascendant_verified_external"]=True
            with self.subTest(case=kind),self.assertRaises(ValueError):
                interpret_profection(bogus)

    def test_static_reference_is_safe_and_short(self):
        txt=profection_house_glossary()
        self.assertLess(len(txt),4096)
        self.assertEqual(txt.count("<b>အိမ် "),12)
        self.assertIn("၁၂ နှစ်",txt)
        self.assertNotIn("2005-12-23",txt)
        self.assertNotIn("\\n",txt)

    def test_wrong_report_rejected(self):
        base=profection_reading(date(2005,12,23),date(2026,10,29),"Aries")
        r=interpret_profection(base)
        r["topic_title"]="အတည်မပြုနိုင်သော အနက်"
        with self.assertRaises(ValueError):
            render_profection_report(base,r)
        with self.assertRaises(ValueError):
            interpret_profection({"house":1})

    def test_traditional_not_modern_planet_swap(self):
        for sign,ruler in (("Scorpio","Mars"),("Aquarius","Saturn"),("Pisces","Jupiter")):
            chart=profection_reading(date(2000,1,1),date(2000,1,1),sign)
            self.assertEqual(interpret_profection(chart)["traditional_ruler"],ruler)

if __name__=="__main__":
    unittest.main()
