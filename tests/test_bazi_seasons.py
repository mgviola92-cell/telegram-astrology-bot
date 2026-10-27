import copy
import unittest
from datetime import datetime
from bazi_core import calculate_bazi
from bazi_seasons import (
    SEASONS, season_for_month_branch, complete_seasonal_memberships,
    calculate_bazi_seasons,
)

class BaziSeasonResearchTests(unittest.TestCase):
    def test_all_twelve_month_branches_covered_once(self):
        all_branches=[b for group in SEASONS for b in group["branches"]]
        self.assertEqual(len(all_branches),12)
        self.assertEqual(len(set(all_branches)),12)
        for group in SEASONS:
            for i,b in enumerate(group["branches"]):
                with self.subTest(b=b):
                    info=season_for_month_branch(b)
                    self.assertEqual(info["name"],group["name"])
                    self.assertEqual(info["phase"],group["phase"])
                    self.assertEqual(info["season_stage"],("early","middle","late")[i])

    def test_full_three_branch_membership_is_distinct(self):
        complete=complete_seasonal_memberships({
            "year":"寅","month":"卯","day":"辰","hour":"卯"
        })
        self.assertEqual(complete[0]["season"],"Spring")
        self.assertEqual(len(complete),1)
        missing=complete_seasonal_memberships({
            "year":"寅","month":"卯","day":"卯","hour":"子"
        })
        self.assertEqual(missing,[])

    def test_all_four_membership_groups(self):
        for group in SEASONS:
            b=group["branches"]
            result=complete_seasonal_memberships({
                "year":b[0],"month":b[1],"day":b[2],"hour":b[0]
            })
            self.assertEqual([x["season"] for x in result],[group["name"]])

    def test_real_lunar_python_chart(self):
        chart=calculate_bazi(datetime(2005,12,23,8,37),
                             timezone_verified="Asia/Yangon")
        result=calculate_bazi_seasons(chart)
        self.assertEqual(chart["pillars"]["month"],"戊子")
        self.assertEqual(result["month"]["name"],"Winter")
        self.assertEqual(result["month"]["phase"],"Water")
        self.assertEqual(result["month"]["month_branch"],"子")
        self.assertEqual(result["day_master_element"],"Metal")
        self.assertFalse(result["day_master_strength_calculated"])
        self.assertFalse(result["prediction_supported"])
        self.assertFalse(result["combination_transformation_claimed"])

    def test_midmonth_library_seasons_across_all_months(self):
        seen=set()
        for month in range(1,13):
            chart=calculate_bazi(datetime(2024,month,15,12),
                                 timezone_verified="Asia/Yangon")
            result=calculate_bazi_seasons(chart)
            branch=chart["pillars"]["month"][1]
            self.assertEqual(result["month"]["month_branch"],branch)
            self.assertEqual(result["evidence"]["derived_facts"]["month_branch"],branch)
            seen.add(branch)
        self.assertEqual(len(seen),12)

    def test_invalid_synthetic_branch(self):
        with self.assertRaises(ValueError):
            season_for_month_branch("nonsense")
        with self.assertRaises(ValueError):
            complete_seasonal_memberships({"year":"子"})

    def test_modified_month_pillar_rejected(self):
        chart=calculate_bazi(datetime(2005,12,23,8,37),
                             timezone_verified="Asia/Yangon")
        altered=copy.deepcopy(chart)
        altered["pillars"]["month"]="甲寅"
        with self.assertRaises(ValueError):
            calculate_bazi_seasons(altered)

if __name__=="__main__":
    unittest.main()
