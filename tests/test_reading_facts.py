import unittest
from reading_facts import reading_facts

class ReadingFactsTests(unittest.TestCase):
    def test_numerology(self):
        data={"number":11,"evidence":{"rule_id":"NUM-PYT-LIFE-PATH-001","derived_facts":{"number":11}}}
        result=reading_facts("numerology",data)
        self.assertEqual(result["facts"]["life_path"],11)
        self.assertFalse(result["prediction_supported"])
    def test_no_evidence(self):
        with self.assertRaises(ValueError):
            reading_facts("numerology",{"number":11})
    def test_invalid_number(self):
        with self.assertRaises(ValueError):
            reading_facts("numerology",{"number":99,"evidence":{"rule_id":"NUM-PYT-LIFE-PATH-001","derived_facts":{}}})
if __name__=="__main__":
    unittest.main()
