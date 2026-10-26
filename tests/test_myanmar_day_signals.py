import unittest
from datetime import date,timedelta
from myanmar_calendar import calculate_myanmar_calendar
from myanmar_day_signals import calculate_day_signals,effective_month,DIRECTIONS,NAKHAT_NAMES

BOOL_MARKERS={
    "sabbath","sabbath_eve","yatyaza","thamanyo","amyeittasote",
    "warameittugyi","warameittunge","yatpote","thamaphyu","nagapor",
    "yatyotema","mahayatkyan","shanyat",
}

class MyanmarDaySignalsTests(unittest.TestCase):
    def test_first_waso_and_late_month_normalization(self):
        self.assertEqual(effective_month(0),4)
        self.assertEqual(effective_month(13),1)
        self.assertEqual(effective_month(14),2)
        with self.assertRaises(ValueError):
            effective_month(15)

    def test_primary_reference_yatyaza_and_pyathada_weekday_tables(self):
        yatyaza={1:{4,6},2:{5,0},3:{3,5},0:{1,4}}
        pyathada={1:{5:1,0:1},2:{4:1,6:1},
                  3:{1:1,2:1},0:{3:1,4:2}}
        seen={k:set() for k in range(4)}
        day=date(2024,1,1)
        while day.year <= 2026:
            cal=calculate_myanmar_calendar(day)
            signals=calculate_day_signals(day)
            month=effective_month(cal["month_index"])
            group=month%4
            wd=(day.weekday()+2)%7
            expected_yat=wd in yatyaza[group]
            expected_pya=pyathada[group].get(wd,0)
            self.assertEqual(signals["markers"]["yatyaza"],expected_yat)
            self.assertEqual(signals["markers"]["pyathada"],expected_pya)
            self.assertEqual(signals["markers"]["nagahle"],(month%12)//3)
            self.assertEqual(signals["markers"]["nakhat"],cal["myanmar_year"]%3)
            seen[group].add(wd)
            day+=timedelta(days=1)
        self.assertTrue(all(len(wds)==7 for wds in seen.values()))

    def test_sabbath_and_sabbath_eve_lunar_dates(self):
        day=date(2025,1,1)
        end=date(2026,1,1)
        sabbaths=0
        while day<end:
            cal=calculate_myanmar_calendar(day)
            signals=calculate_day_signals(day)
            md=cal["day"]
            ml=signals["lunar_month_length"]
            self.assertEqual(signals["markers"]["sabbath"],md in (8,15,23,ml))
            self.assertEqual(signals["markers"]["sabbath_eve"],md in (7,14,22,ml-1))
            sabbaths+=int(signals["markers"]["sabbath"])
            day+=timedelta(days=1)
        self.assertGreater(sabbaths,40)

    def test_independent_mmcal_cpp_2024_jan1_golden_vector(self):
        # yan9a/mmcal cpp/test/cedate/cedate.cpp published regression.
        cal=calculate_myanmar_calendar(date(2024,1,1))
        result=calculate_day_signals(date(2024,1,1))
        self.assertEqual((cal["myanmar_year"],cal["month_index"],cal["day"]),
                         (1385,9,20))
        self.assertEqual(result["nagahle_direction"],"တောင်")
        self.assertFalse(any(result["markers"][name] for name in BOOL_MARKERS))
        self.assertEqual(result["markers"]["pyathada"],0)

    def test_evidence_and_labels_all_days(self):
        for day in (date(1900,1,1),date(1990,5,14),date(2024,1,1),
                    date(2026,10,27),date(2099,10,27),date(2100,12,30)):
            with self.subTest(day=day):
                got=calculate_day_signals(day)
                self.assertEqual(got["evidence"]["derived_facts"],got["markers"])
                self.assertEqual(got["evidence"]["input_assumptions"]["local_gregorian_date"],day.isoformat())
                self.assertEqual(set(got["markers"]),BOOL_MARKERS|{"pyathada","nagahle","nakhat"})
                self.assertTrue(all(type(got["markers"][k]) is bool for k in BOOL_MARKERS))
                self.assertIn(got["markers"]["pyathada"],(0,1,2))
                self.assertIn(got["nagahle_direction"],DIRECTIONS)
                self.assertIn(got["nakhat_name"],NAKHAT_NAMES)
                self.assertFalse(got["prediction_supported"])

if __name__=="__main__":
    unittest.main()
