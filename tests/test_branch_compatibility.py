"""All 144 two-branch relationships, privacy and strict lookup provenance."""
import copy
import unittest
from bazi_elements import BRANCHES
from branch_compatibility import (
    ANIMALS,LIUHE,LIUCHONG,SANHE,RULE_ID,
    compare_branches,render_branch_comparison,branch_picker,
)

class BranchCompatibilityTests(unittest.TestCase):
    def test_all_orderings_symmetric_and_never_predictive(self):
        branches=tuple(BRANCHES)
        self.assertEqual(len(branches),12)
        for a in branches:
            for b in branches:
                with self.subTest(a=a,b=b):
                    x=compare_branches(a,b)
                    y=compare_branches(b,a)
                    self.assertEqual(x["matches"],y["matches"])
                    self.assertEqual(x["rule_id"],RULE_ID)
                    self.assertFalse(x["compatibility_score_computed"])
                    self.assertFalse(x["calendar_birth_year_derived"])
                    self.assertFalse(x["full_four_pillars_compared"])
                    self.assertFalse(x["prediction_supported"])
                    self.assertFalse(x["personal_data_saved"])
                    msg=render_branch_comparison(x)
                    self.assertLess(len(msg),4096)
                    self.assertNotIn("\\n",msg)
                    self.assertNotIn("2005-12-23",msg)

    def test_traditional_pair_tables_all_six_each(self):
        self.assertEqual(len(LIUHE),6)
        self.assertEqual(len(LIUCHONG),6)
        for a,b in LIUHE:
            self.assertIn("liuhe",[m["category"] for m in compare_branches(a,b)["matches"]])
            self.assertNotIn("liuchong",[m["category"] for m in compare_branches(a,b)["matches"]])
        for a,b in LIUCHONG:
            self.assertIn("liuchong",[m["category"] for m in compare_branches(a,b)["matches"]])
            self.assertNotIn("liuhe",[m["category"] for m in compare_branches(a,b)["matches"]])

    def test_two_of_a_trine_does_not_claim_three(self):
        for phase,group in SANHE.items():
            for a,b in ((group[0],group[1]),(group[1],group[2]),(group[0],group[2])):
                with self.subTest(phase=phase,a=a,b=b):
                    matches=compare_branches(a,b)["matches"]
                    triple=[x for x in matches if x["category"]=="sanhe_partial"]
                    self.assertEqual(len(triple),1)
                    self.assertEqual(triple[0]["full_group"],"".join(group))
                    self.assertIn("မဖွဲ့ပါ",triple[0]["explanation"])

    def test_same_symbol_and_no_named_match_distinct(self):
        same=compare_branches("子","子")
        self.assertEqual([x["category"] for x in same["matches"]],["same"])
        self.assertIn("တူညီသော",render_branch_comparison(same))
        other=compare_branches("子","巳")
        self.assertEqual(other["matches"],[])
        self.assertIn("မတွေ့ပါ",render_branch_comparison(other))

    def test_malformed_or_forged_result_rejected(self):
        for a,b in (("Rat","丑"),("子","x"),(" 子","丑"),("",None)):
            with self.subTest(a=a,b=b),self.assertRaises(ValueError):
                compare_branches(a,b)
        valid=compare_branches("子","丑")
        for key in ("first_animal","matches","scope","prediction_supported"):
            modified=copy.deepcopy(valid)
            if key=="matches":modified[key]=[]
            elif key=="prediction_supported":modified[key]=True
            else:modified[key]="fake"
            with self.subTest(key=key),self.assertRaises(ValueError):
                render_branch_comparison(modified)

    def test_native_picker_no_date_and_telegram_callback_size(self):
        first=branch_picker("first")
        self.assertEqual([len(row) for row in first],[3,3,3,3,1])
        self.assertEqual({button.split(":")[-1] for row in first[:-1] for _,button in row},set(ANIMALS))
        for a in ANIMALS:
            second=branch_picker("second",a)
            self.assertEqual([len(row) for row in second],[3,3,3,3,1])
            for row in second:
                for label,callback in row:
                    self.assertLessEqual(len(callback.encode("utf-8")),64)
                    self.assertTrue(label)
                    self.assertNotIn("2005",callback)
        with self.assertRaises(ValueError):branch_picker("second","notbranch")
        with self.assertRaises(ValueError):branch_picker("unknown")

if __name__=="__main__":
    unittest.main()
