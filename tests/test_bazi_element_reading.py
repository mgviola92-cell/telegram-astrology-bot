import copy
import unittest
from datetime import datetime
from bazi_core import calculate_bazi
from bazi_element_reading import bazi_element_reading,relationship
from bazi_elements import ELEMENTS

class BaziElementReadingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chart=calculate_bazi(datetime(2005,12,23,8,37),timezone_verified="Asia/Yangon")

    def test_all_five_relationships(self):
        expected={"Wood":"same","Fire":"day_generates","Earth":"day_controls",
                  "Metal":"controls_day","Water":"generates_day"}
        for element,relation in expected.items():
            self.assertEqual(relationship("Wood",element),relation)

    def test_all_element_pairs_have_relationship(self):
        for day in ELEMENTS:
            self.assertEqual({relationship(day,other) for other in ELEMENTS},
                             {"same","day_generates","generates_day","day_controls","controls_day"})

    def test_upstream_chart_consistency(self):
        result=bazi_element_reading(self.chart)
        self.assertEqual(result["day_master"],"辛")
        self.assertEqual(result["day_element"],"Metal")
        self.assertEqual(result["polarity"],"Yin")
        self.assertEqual(sum(x["visible_count"] for x in result["groups"]),8)
        self.assertEqual(len(result["groups"]),5)
        self.assertFalse(result["prediction_supported"])
        self.assertFalse(result["seasonal_strength_calculated"])

    def test_reject_modified_elements(self):
        modified=copy.deepcopy(self.chart)
        modified["visible_wuxing"]["visible_counts"]["Wood"]+=1
        with self.assertRaises(ValueError):
            bazi_element_reading(modified)

    def test_reject_modified_day_master(self):
        modified=copy.deepcopy(self.chart)
        modified["day_master"]="甲"
        with self.assertRaises(ValueError):
            bazi_element_reading(modified)

    def test_reject_unknown_element(self):
        with self.assertRaises(ValueError):
            relationship("Aether","Water")

if __name__=="__main__":
    unittest.main()
