"""Source-checked ten-god functional families, day-stem roles and safety."""
import copy
import unittest
from datetime import datetime
from bazi_core import calculate_bazi
from bazi_ten_gods import ten_god
from bazi_elements import STEMS,ELEMENTS
from bazi_ten_gods_reading import (
    FAMILIES,SYMBOL_NAMES,FAMILY_FOR_SYMBOL,RULE_ID,_family_elements,
    interpret_ten_gods,summarize_ten_gods_burmese,
)

class TenGodInterpretationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chart=calculate_bazi(datetime(2005,12,23,8,37),timezone_verified="Asia/Yangon")

    def test_ten_symbols_unique_and_five_pairs_complete(self):
        self.assertEqual(len(FAMILIES),5)
        self.assertEqual(len(SYMBOL_NAMES),10)
        self.assertEqual(len(FAMILY_FOR_SYMBOL),10)
        all_symbols=[symbol for pair in FAMILIES.values() for symbol in pair["symbols"]]
        self.assertEqual(len(all_symbols),len(set(all_symbols)))
        for day in STEMS:
            observed={ten_god(day,other) for other in STEMS}
            self.assertEqual(set(all_symbols),observed)

    def test_each_phase_has_complete_five_family_mapping(self):
        for element in ELEMENTS:
            with self.subTest(element=element):
                families=_family_elements(element)
                self.assertEqual(set(families),set(FAMILIES))
                self.assertEqual(set(families.values()),set(ELEMENTS))

    def test_verified_reference_chart_and_visible_pillars(self):
        result=interpret_ten_gods(self.chart)
        self.assertEqual(result["day_master"],"辛")
        self.assertEqual(result["day_element"],"Metal")
        self.assertEqual(result["day_polarity"],"Yin")
        self.assertEqual([(x["pillar"],x["ten_god"]) for x in result["visible"]],
                         [("year","偏财"),("month","正印"),("hour","伤官")])
        self.assertEqual(len(result["families"]),5)
        self.assertGreater(len(result["hidden"]),4)
        self.assertFalse(result["day_master_strength_inferred"])
        self.assertFalse(result["hidden_stem_weights_inferred"])
        self.assertFalse(result["prediction_supported"])
        self.assertFalse(result["profile_saved"])
        self.assertEqual(result["rule_id"],RULE_ID)
        text=summarize_ten_gods_burmese(result)
        self.assertIn("ရက်တိုင် 辛",text)
        self.assertIn("偏财",text)
        self.assertIn("正印",text)
        self.assertIn("伤官",text)
        self.assertIn("သတ္တု",text)
        self.assertIn("ရိုးရာ ဓာတ်ဆက်နွယ်မှု ၅ အုပ်စု",text)
        self.assertLess(len(text),1300)
        self.assertNotIn("2005-12-23",text)
        self.assertNotIn("08:37",text)
        self.assertNotIn("\\n",text)

    def test_tampered_pillars_hidden_stems_or_evidence_rejected(self):
        for mutated in ("pillars","ten_gods_all","day_master","evidence"):
            fake=copy.deepcopy(self.chart)
            if mutated=="pillars":
                fake["pillars"]["year"]="甲子"
            elif mutated=="ten_gods_all":
                fake["ten_gods_all"]["hidden"]["day"][0]["ten_god"]="正财"
            elif mutated=="day_master":
                fake["day_master"]="乙"
            else:
                fake["evidence"]["derived_facts"]["pillars"]["month"]="乙亥"
            with self.subTest(mutation=mutated),self.assertRaises(ValueError):
                interpret_ten_gods(fake)

    def test_incomplete_or_fake_reading_rejected_for_summary(self):
        r=interpret_ten_gods(self.chart)
        with self.assertRaises(ValueError):
            summarize_ten_gods_burmese({})
        r["visible"].pop()
        with self.assertRaises(ValueError):
            summarize_ten_gods_burmese(r)

    def test_day_master_is_not_reported_as_independent_other_stem(self):
        result=interpret_ten_gods(self.chart)
        self.assertNotIn("day",[x["pillar"] for x in result["visible"]])
        self.assertEqual(result["visible"][0]["stem"],self.chart["pillars"]["year"][0])

if __name__=="__main__":
    unittest.main()
