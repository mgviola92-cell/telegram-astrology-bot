import unittest
from datetime import date, datetime
from daily_calendar_reading import daily_calendar_reading, DAILY_RULE_ID
from myanmar_day_signals import calculate_day_signals

class DailyCalendarReadingTests(unittest.TestCase):
    def test_known_published_2026_thadingyut_calendar_vectors(self):
        # Yan Naing Aye's online 2026 Oct calendar shows:
        # 27 Oct Yatyaza; 28 Oct no headline day; 29 Oct Yatyaza.
        for day,expected_yatyaza in (
            (date(2026,10,27),True),
            (date(2026,10,28),False),
            (date(2026,10,29),True),
        ):
            with self.subTest(day=day):
                reading=daily_calendar_reading(day)
                self.assertEqual("ရက်ရာဇာ" in reading["active_labels"],expected_yatyaza)
                self.assertEqual(reading["interpretation_rule_id"],DAILY_RULE_ID)
                self.assertFalse(reading["prediction_supported"])
                self.assertFalse(reading["personalized"])

    def test_same_date_is_deterministic_without_randomness(self):
        original=daily_calendar_reading(date(2024,1,1))
        self.assertEqual(original,daily_calendar_reading(date(2024,1,1)))
        self.assertEqual(original["calculation_rule_id"],"MM-CALENDAR-DAY-SIGNALS-001")

    def test_reading_labels_are_exactly_verified_day_markers(self):
        from myanmar_signal_reading import describe_day_signals
        for year in (2000,2024,2026,2035):
            for month in range(1,13):
                day=date(year,month,15)
                result=daily_calendar_reading(day)
                source=describe_day_signals(calculate_day_signals(day))
                self.assertEqual(result["active_labels"],source["active_labels"])
                self.assertEqual(result["nagahle_direction"],source["nagahle_direction"])

    def test_reject_invalid_birth_or_unbounded_day_inputs(self):
        for invalid in (datetime(2026,10,28),date(1899,1,1),date(2101,1,1),
                        "2026-10-28",None):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    daily_calendar_reading(invalid)

if __name__=="__main__":
    unittest.main()
