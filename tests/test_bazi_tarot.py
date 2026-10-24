import unittest
from datetime import datetime
from tarot_core import DECK, draw_tarot
from bazi_core import calculate_bazi

class TarotTests(unittest.TestCase):
    def test_deck(self):
        self.assertEqual(len(DECK), 78)
        self.assertEqual(len(set(DECK)), 78)
    def test_draw_unique(self):
        result=draw_tarot('three')
        self.assertEqual(len(result['cards']), 3)
        self.assertEqual(len({c['card'] for c in result['cards']}),3)
        self.assertIn('rule_id',result['evidence'])
    def test_bad_spread(self):
        with self.assertRaises(ValueError): draw_tarot('seven')

class BaziTests(unittest.TestCase):
    def test_upstream_reference(self):
        try: import lunar_python
        except ImportError: self.skipTest('optional lunar-python not installed')
        p=calculate_bazi(datetime(2005,12,23,8,37))['pillars']
        self.assertEqual(p,{'year':'乙酉','month':'戊子','day':'辛巳','hour':'壬辰'})
    def test_reject_timezone_aware(self):
        from datetime import timezone
        with self.assertRaises(ValueError): calculate_bazi(datetime(2000,1,1,tzinfo=timezone.utc))
    def test_primary_element_tally_on_upstream_vector(self):
        try: import lunar_python
        except ImportError: self.skipTest('lunar-python not installed')
        result=calculate_bazi(datetime(2005,12,23,8,37))
        visible=result['visible_wuxing']
        self.assertEqual(visible['visible_counts'],{'Wood':1,'Fire':1,'Earth':2,'Metal':2,'Water':2})
        self.assertEqual(visible['day_master_element'],'Metal')
        self.assertEqual(result['pillars']['day'],'辛巳')
    def test_declared_timezone_passes_to_provenance(self):
        try: import lunar_python
        except ImportError: self.skipTest('lunar-python not installed')
        result=calculate_bazi(datetime(2005,12,23,8,37),timezone_verified='Asia/Yangon')
        self.assertEqual(result['evidence']['input_assumptions']['timezone_verified'],'Asia/Yangon')
    def test_hidden_stems_match_upstream_getters(self):
        try:
            from lunar_python import Solar
        except ImportError:
            self.skipTest("lunar-python missing")
        solar=Solar.fromYmdHms(2005,12,23,8,37)
        upstream=solar.getLunar().getEightChar()
        local=calculate_bazi(datetime(2005,12,23,8,37))
        got=local["hidden_stems"]["pillars"]
        for name,getter in (("year",upstream.getYearHideGan),
                            ("month",upstream.getMonthHideGan),
                            ("day",upstream.getDayHideGan),
                            ("hour",upstream.getTimeHideGan)):
            with self.subTest(pillar=name):
                self.assertEqual([entry["stem"] for entry in got[name]["hidden"]],list(getter()))

    def test_ten_gods_match_upstream_stems(self):
        try:
            from lunar_python import Solar
            from lunar_python.util import LunarUtil
        except ImportError:
            self.skipTest("lunar-python missing")
        upstream=Solar.fromYmdHms(2005,12,23,8,37).getLunar().getEightChar()
        result=calculate_bazi(datetime(2005,12,23,8,37))
        day=upstream.getDayGan()
        gods=result["ten_gods_all"]
        for name,pillar in result["pillars"].items():
            with self.subTest(pillar=name):
                self.assertEqual(gods["visible"][name]["ten_god"],
                                 LunarUtil.SHI_SHEN[day+pillar[0]])
                self.assertEqual(
                    [g["ten_god"] for g in gods["hidden"][name]],
                    [LunarUtil.SHI_SHEN[day+g] for g in
                     {"year":upstream.getYearHideGan,
                      "month":upstream.getMonthHideGan,
                      "day":upstream.getDayHideGan,
                      "hour":upstream.getTimeHideGan}[name]()])

    def test_invalid_sect(self):
        with self.assertRaises(ValueError): calculate_bazi(datetime(2000,1,1),sect=3)

if __name__=='__main__': unittest.main()
