"""Weekly Myanmar cultural calendar: sources, bounds, cache and callback safety."""
import unittest
from datetime import date, timedelta
from unittest.mock import patch
from weekly_calendar import (
    WEEKDAYS, week_start, valid_week, parse_week_callback,
    week_actions, week_text,
)

class WeeklyCalendarTests(unittest.TestCase):
    def setUp(self):
        week_text.cache_clear()

    def test_week_anchored_on_monday_with_exact_seven_days(self):
        monday=date(2026,10,26)
        self.assertEqual(week_start(date(2026,10,29)),monday)
        output=week_text(monday)
        self.assertIn("2026-10-26",output)
        self.assertIn("2026-11-01",output)
        self.assertEqual(len(WEEKDAYS),7)
        for number in range(7):
            with self.subTest(number=number):
                self.assertIn((monday+timedelta(days=number)).isoformat(),output)
        self.assertIn("ရက်ရာဇာ",output)
        self.assertIn("ကိုယ်ပိုင်မွေးဇာတာ",output)
        self.assertNotIn("\\n",output)
        self.assertLess(len(output),4096)

    def test_week_crosses_year_boundary(self):
        start=week_start(date(2026,12,31))
        rendered=week_text(start)
        self.assertIn("2026-12-28",rendered)
        self.assertIn("2027-01-03",rendered)

    def test_no_member_or_birth_specific_data_in_cache(self):
        week_text(date(2026,10,26))
        week_text(date(2026,10,26))
        self.assertEqual(week_text.cache_info().maxsize,8)
        self.assertEqual(week_text.cache_info().misses,1)
        self.assertEqual(week_text.cache_info().hits,1)

    def test_nearby_weeks_only_and_callback_input_is_strict(self):
        today=date(2026,10,29)
        this=week_start(today)
        self.assertTrue(valid_week(this,today=today))
        callbacks=[value for _,value in week_actions(this,today=today)]
        self.assertEqual(len(callbacks),3)
        for value in callbacks:
            self.assertEqual(parse_week_callback(value,today=today).weekday(),0)
            self.assertLessEqual(len(value.encode("utf8")),64)
        bad=[
            "calendarweek:2026-11-09", "calendarweek:2026-10-28",
            "calendarweek:2005-12-26", "calendarweek:2026-13-40",
            "calendarweek:2026-10-26:123", "calendarweek:2026-10-26T11:00",
            "calendar:2026-10-26",
        ]
        for value in bad:
            with self.subTest(value=value),self.assertRaises(ValueError):
                parse_week_callback(value,today=today)
        end=week_start(today)+timedelta(days=7)
        self.assertFalse(any(value.endswith("2026-11-09") for _,value in week_actions(end,today=today)))

    def test_old_week_button_expires_after_two_weeks(self):
        old="calendarweek:2026-10-19"
        self.assertEqual(parse_week_callback(old,today=date(2026,10,29)),date(2026,10,19))
        with self.assertRaises(ValueError):
            parse_week_callback(old,today=date(2026,11,9))

    def test_private_data_fail_closed(self):
        monday=date(2026,10,26)
        with patch("weekly_calendar.daily_calendar_reading",
                   return_value={"personalized":True,"prediction_supported":False}):
            with self.assertRaises(ValueError):
                week_text(monday)

    def test_reject_non_monday_and_bad_year(self):
        for bad in (date(2026,10,27),date(1899,12,25)):
            with self.subTest(bad=bad),self.assertRaises(ValueError):
                week_text(bad)
        with self.assertRaises(ValueError):
            week_start("2026-10-29")

if __name__=="__main__":
    unittest.main()
