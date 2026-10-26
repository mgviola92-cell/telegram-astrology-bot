import copy
import unittest
from datetime import datetime
from lunar_python import Solar
from bazi_core import calculate_bazi
from bazi_growth_stages import calculate_growth_stages,STAGE_NAMES,STAGE_GLOSSES

class BaziGrowthStagesTests(unittest.TestCase):
    def test_all_twelve_names_have_conservative_burmese_glosses(self):
        self.assertEqual(len(STAGE_NAMES),12)
        self.assertEqual(len(set(STAGE_NAMES)),12)
        self.assertEqual(set(STAGE_NAMES),set(STAGE_GLOSSES))

    def test_upstream_four_stage_getters_on_reference_chart(self):
        for sect in (1,2):
            with self.subTest(sect=sect):
                moment=datetime(2005,12,23,8,37)
                chart=calculate_bazi(moment,sect=sect,timezone_verified="Asia/Yangon")
                calculated=calculate_growth_stages(chart)
                upstream=Solar.fromYmdHms(2005,12,23,8,37,0).getLunar().getEightChar()
                upstream.setSect(sect)
                expected={
                    "year":upstream.getYearDiShi(),
                    "month":upstream.getMonthDiShi(),
                    "day":upstream.getDayDiShi(),
                    "hour":upstream.getTimeDiShi(),
                }
                self.assertEqual(calculated["stages"],expected)
                self.assertEqual(set(calculated["burmese_stage_names"]),set(expected))
                self.assertFalse(calculated["prediction_supported"])
                self.assertFalse(calculated["seasonal_strength_calculated"])
                self.assertEqual(calculated["evidence"]["derived_facts"]["stages"],expected)

    def test_late_night_sect_boundary(self):
        moment=datetime(2024,1,23,23,40)
        for sect in (1,2):
            with self.subTest(sect=sect):
                chart=calculate_bazi(moment,sect=sect,timezone_verified="Asia/Yangon")
                calculated=calculate_growth_stages(chart)
                self.assertEqual(calculated["day_master"],chart["day_master"])
                self.assertEqual(set(calculated["stages"]),{"year","month","day","hour"})

    def test_modified_day_pillar_rejected(self):
        chart=calculate_bazi(datetime(2005,12,23,8,37),timezone_verified="Asia/Yangon")
        altered=copy.deepcopy(chart)
        altered["pillars"]["day"]="甲子"
        with self.assertRaises(ValueError):
            calculate_growth_stages(altered)

    def test_missing_input_provenance_rejected(self):
        chart=calculate_bazi(datetime(2005,12,23,8,37),timezone_verified="Asia/Yangon")
        del chart["evidence"]["input_assumptions"]["sect"]
        with self.assertRaises((KeyError,ValueError)):
            calculate_growth_stages(chart)

if __name__=="__main__":
    unittest.main()
