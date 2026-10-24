import unittest
from bazi_elements import STEMS, BRANCHES, summarize_visible_elements

class VisibleFivePhasesTests(unittest.TestCase):
    def setUp(self):
        self.p={"year":"乙酉","month":"戊子","day":"辛巳","hour":"壬辰"}
    def test_reference_eight_visible_symbols(self):
        result=summarize_visible_elements(self.p)
        self.assertEqual(result["visible_counts"],{"Wood":1,"Fire":1,"Earth":2,"Metal":2,"Water":2})
        self.assertEqual(sum(result["visible_counts"].values()),8)
        self.assertEqual(result["day_master_element"],"Metal")
        self.assertEqual(result["day_master_polarity"],"Yin")
    def test_complete_stem_branch_tables(self):
        self.assertEqual(len(STEMS),10)
        self.assertEqual(len(BRANCHES),12)
    def test_invalid_missing_hour(self):
        with self.assertRaises(ValueError):
            summarize_visible_elements({"year":"乙酉","month":"戊子","day":"辛巳"})
    def test_invalid_parity(self):
        with self.assertRaisesRegex(ValueError,"parity"):
            summarize_visible_elements(dict(self.p,day="甲丑"))
    def test_unknown_character(self):
        with self.assertRaises(ValueError):
            summarize_visible_elements(dict(self.p,year="X酉"))
    def test_no_strength_claim(self):
        result=summarize_visible_elements(self.p)
        self.assertFalse(result["evidence"]["input_assumptions"]["seasonal_strength_calculated"])
        self.assertFalse(result["evidence"]["input_assumptions"]["hidden_stems_included"])
if __name__=="__main__":unittest.main()
