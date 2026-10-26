import copy
import unittest
from datetime import date
from myanmar_calendar import calculate_myanmar_calendar
from myanmar_day_reading import calendar_marker_reading

class CalendarInterpretationTests(unittest.TestCase):
    def test_many_dates_derive_appropriate_marker(self):
        checked=0
        for year in (2020,2024,2026):
            for month in range(1,13):
                for day in (1,8,15,22):
                    try:
                        result=calculate_myanmar_calendar(date(year,month,day))
                    except ValueError:
                        continue
                    reading=calendar_marker_reading(result)
                    keys={entry["key"] for entry in reading["markers"]}
                    self.assertEqual("yatyaza" in keys,result["yatyaza"])
                    self.assertEqual("pyathada" in keys,result["pyathada"]==1)
                    self.assertEqual("afternoon_pyathada" in keys,result["pyathada"]==2)
                    self.assertEqual("ordinary" in keys,not result["yatyaza"] and not result["pyathada"])
                    self.assertFalse(reading["prediction_supported"])
                    self.assertTrue(all(entry["rule_id"]==reading["rule_id"] for entry in reading["markers"]))
                    checked+=1
        self.assertGreater(checked,100)
    def test_tampered_calendar_rejected(self):
        result=calculate_myanmar_calendar(date(2024,1,1))
        bad=copy.deepcopy(result)
        bad["yatyaza"]=not bad["yatyaza"]
        with self.assertRaises(ValueError):
            calendar_marker_reading(bad)
    def test_no_birth_or_personal_fate_claim(self):
        reading=calendar_marker_reading(calculate_myanmar_calendar(date(2024,1,1)))
        self.assertEqual(reading["category"],"traditional_calendar_day_markers")
        self.assertFalse(reading["prediction_supported"])

if __name__=="__main__":
    unittest.main()
