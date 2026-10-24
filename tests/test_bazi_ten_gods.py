import unittest
from bazi_ten_gods import ten_god, calculate_ten_gods

class TenGodTests(unittest.TestCase):
    def test_ten_relations(self):
        reference={"甲":"比肩","乙":"劫财","丙":"食神","丁":"伤官",
                   "戊":"偏财","己":"正财","庚":"七杀","辛":"正官",
                   "壬":"偏印","癸":"正印"}
        for stem,expected in reference.items():
            with self.subTest(stem=stem):
                self.assertEqual(ten_god("甲",stem),expected)
    def test_every_day_stem_has_ten_distinct_relations(self):
        stems="甲乙丙丁戊己庚辛壬癸"
        for day in stems:
            with self.subTest(day=day):
                self.assertEqual(len({ten_god(day,s) for s in stems}),10)
    def test_invalid(self):
        with self.assertRaises(ValueError):ten_god("X","甲")
    def test_reference_four_pillars(self):
        p={"year":"乙酉","month":"戊子","day":"辛巳","hour":"壬辰"}
        v=calculate_ten_gods(p)
        self.assertEqual(v["visible"]["year"]["ten_god"],"偏财")
        self.assertEqual(v["visible"]["month"]["ten_god"],"正印")
        self.assertEqual(v["visible"]["hour"]["ten_god"],"伤官")
        self.assertEqual(v["hidden"]["year"][0]["ten_god"],"比肩")
        self.assertEqual(len(v["hidden"]["day"]),3)
        self.assertFalse(v["evidence"]["input_assumptions"]["fortune_forecast_inferred"])
    def test_upstream_table_all_hundred_combinations(self):
        try:from lunar_python.util import LunarUtil
        except ImportError:self.skipTest("lunar-python is not available")
        for a in "甲乙丙丁戊己庚辛壬癸":
            for b in "甲乙丙丁戊己庚辛壬癸":
                with self.subTest(day=a,other=b):
                    self.assertEqual(ten_god(a,b),LunarUtil.SHI_SHEN[a+b])
if __name__=="__main__":unittest.main()
