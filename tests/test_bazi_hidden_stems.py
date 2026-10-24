import unittest
from bazi_hidden_stems import HIDDEN_STEMS, calculate_hidden_stems

class HiddenStemTests(unittest.TestCase):
 def setUp(self):
    self.p={"year":"乙酉","month":"戊子","day":"辛巳","hour":"壬辰"}
 def test_source_table_is_complete(self):
    self.assertEqual(len(HIDDEN_STEMS),12)
    self.assertEqual(HIDDEN_STEMS["子"],("癸",))
    self.assertEqual(HIDDEN_STEMS["辰"],("戊","乙","癸"))
 def test_reference_pillars(self):
    v=calculate_hidden_stems(self.p)
    self.assertEqual([x["stem"] for x in v["pillars"]["year"]["hidden"]],["辛"])
    self.assertEqual([x["stem"] for x in v["pillars"]["month"]["hidden"]],["癸"])
    self.assertEqual([x["stem"] for x in v["pillars"]["day"]["hidden"]],["丙","庚","戊"])
    self.assertEqual([x["stem"] for x in v["pillars"]["hour"]["hidden"]],["戊","乙","癸"])
 def test_primary_order_not_weights(self):
    v=calculate_hidden_stems(self.p)
    self.assertEqual(v["pillars"]["day"]["hidden"][0]["traditional_order"],"primary")
    self.assertFalse(v["evidence"]["input_assumptions"]["qi_percentages_applied"])
 def test_missing_pillar_rejected(self):
    with self.assertRaises(ValueError):
        calculate_hidden_stems({"year":"乙酉"})
 def test_invalid_parity_rejected(self):
    with self.assertRaises(ValueError):
        calculate_hidden_stems(dict(self.p,day="甲丑"))

if __name__=="__main__":
 unittest.main()
