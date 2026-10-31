import unittest
from datetime import datetime
from copy import deepcopy
from bazi_core import calculate_bazi
from bazi_pairs import classify_pairs,format_pairs,TABLES

class PairRelationTests(unittest.TestCase):
    def test_canonical_sets(self):
        self.assertEqual([len(v) for v in TABLES.values()],[6,6,5])
        for pairs in TABLES.values():
            self.assertEqual(len({frozenset(p) for p in pairs}),len(pairs))

    def test_real_charts(self):
        for year,month,day in ((2005,12,23),(1990,5,14),(2000,1,1),(2024,9,21)):
            chart=calculate_bazi(datetime(year,month,day,8,37),timezone_verified="Asia/Yangon")
            reading=classify_pairs(chart)
            self.assertFalse(reading["predictive_claim"])
            self.assertFalse(reading["phase_transformation_assessed"])
            for item in reading["records"]:
                off=0 if item["type"]=="stem_union" else 1
                p=chart["pillars"]
                self.assertEqual(item["symbols"],p[item["a"]][off]+p[item["b"]][off])
                self.assertIn(frozenset(item["symbols"]),set(map(frozenset,TABLES[item["type"]])))
            text=format_pairs(reading)
            self.assertIn("六冲",text)
            self.assertLess(len(text),1051)
            self.assertNotIn(str(year)+"-",text)

    def test_chart_mutation_rejected(self):
        original=calculate_bazi(datetime(2005,12,23,8,37),timezone_verified="Asia/Yangon")
        changed=deepcopy(original)
        changed["pillars"]["year"]="甲子"
        with self.assertRaises(ValueError):
            classify_pairs(changed)

    def test_reject_forged_relationship_records(self):
        chart=calculate_bazi(datetime(2005,12,23,8,37),timezone_verified="Asia/Yangon")
        genuine=classify_pairs(chart)
        examples=[
            {"type":"branch_union","a":"year","b":"month","symbols":"<b>","adjacent":True},
            {"type":"stem_union","a":"year","b":"month","symbols":"甲己","adjacent":False},
            {"type":"branch_opposite","a":"hour","b":"day","symbols":"子午","adjacent":True},
            {"type":"stem_union","a":"year","b":"month","symbols":"甲己","adjacent":True},
        ]
        for forged in examples:
            with self.subTest(forged=forged):
                bad=deepcopy(genuine)
                bad["records"]=[forged,forged]
                with self.assertRaises(ValueError):
                    format_pairs(bad)

    def test_report_tampering_and_input_validation(self):
        chart=calculate_bazi(datetime(2005,12,23,8,37),timezone_verified="Asia/Yangon")
        good=classify_pairs(chart)
        for field,value in (("rule_id","FAKE"),("predictive_claim",True),
                            ("phase_transformation_assessed",True),
                            ("natal_source_validated",False),
                            ("records",None)):
            with self.subTest(field=field):
                bad=deepcopy(good)
                bad[field]=value
                with self.assertRaises(ValueError):
                    format_pairs(bad)
