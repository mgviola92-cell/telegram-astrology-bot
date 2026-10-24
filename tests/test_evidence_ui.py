import unittest
from evidence_ui import RULES, get_rule

class EvidenceRegistryTests(unittest.TestCase):
    def test_relevant_rules(self):
        for rule in ('NUM-PYT-LIFE-PATH-001','CHN-BAZI-PILLARS-001','MM-8DAY-WEEKDAY-001','TAROT-DRAW-001'):
            data=get_rule(rule)
            self.assertTrue(data['source'])
            self.assertTrue(data['limits'])
    def test_callback_length(self):
        for key in RULES:
            self.assertLessEqual(len(('evidence:'+key).encode('utf8')),64)
    def test_unknown_denied(self):
        with self.assertRaises(KeyError): get_rule('MADE-UP-000')
if __name__=='__main__': unittest.main()
