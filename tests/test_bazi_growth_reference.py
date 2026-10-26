import unittest
from datetime import datetime
from lunar_python import Solar
from bazi_growth_reference import STAGES, BRANCH_ORDER, OFFSETS, stage_for, stages_for_pillars
from bazi_elements import STEMS
from bazi_core import calculate_bazi

class IndependentGrowthReferenceTests(unittest.TestCase):
    def test_all_120_stem_branch_combinations_cover_twelve_stages(self):
        for stem in OFFSETS:
            mapped=[stage_for(stem,branch) for branch in BRANCH_ORDER]
            self.assertEqual(set(mapped),set(STAGES))
            self.assertEqual(len(mapped),12)

    def test_yin_stems_progress_in_opposite_direction(self):
        for stem in OFFSETS:
            step=1 if STEMS[stem][1]=="Yang" else -1
            for i in range(12):
                current=STAGES.index(stage_for(stem,BRANCH_ORDER[i]))
                following=STAGES.index(stage_for(stem,BRANCH_ORDER[(i+1)%12]))
                self.assertEqual((following-current)%12,step%12)

    def test_against_real_upstream_pillars(self):
        for y,m,d,h in ((2005,12,23,8),(2024,1,23,13),
                        (1990,5,14,16),(2026,10,27,9)):
            with self.subTest(y=y,m=m,d=d,h=h):
                chart=calculate_bazi(datetime(y,m,d,h))
                upstream=Solar.fromYmdHms(y,m,d,h,0,0).getLunar().getEightChar()
                upstream.setSect(2)
                got=stages_for_pillars(chart["pillars"],chart["day_master"])
                expected={
                    "year":upstream.getYearDiShi(),
                    "month":upstream.getMonthDiShi(),
                    "day":upstream.getDayDiShi(),
                    "hour":upstream.getTimeDiShi(),
                }
                self.assertEqual(got,expected)

    def test_reject_undocumented_stem_and_branch(self):
        with self.assertRaises(ValueError):
            stage_for("X","子")
        with self.assertRaises(ValueError):
            stage_for("甲","X")

    def test_reject_inconsistent_day_master(self):
        chart=calculate_bazi(datetime(2005,12,23,8,37))
        with self.assertRaises(ValueError):
            stages_for_pillars(chart["pillars"],"甲")

if __name__=="__main__":
    unittest.main()
