"""Source-backed public calendar cards and group traffic guard."""
import unittest
from datetime import date
from unittest.mock import patch
from public_calendar import (
    GroupCalendarGate, NEARBY_DAYS, day_actions,
    myanmar_today, parse_day_callback, public_calendar_text, valid_nearby_day,
)

class PublicCalendarTests(unittest.TestCase):
    def setUp(self):
        public_calendar_text.cache_clear()

    def test_real_calendar_october_2026_is_safe_and_short(self):
        day=date(2026,10,27)
        card=public_calendar_text(day)
        self.assertIn("2026-10-27",card)
        self.assertIn("မြန်မာရိုးရာ",card)
        self.assertIn("ရက်ရာဇာ",card)
        self.assertIn("မွေးဇာတာ",card)
        self.assertNotIn("\\n",card)
        self.assertLess(len(card),1800)
    def test_one_calculation_per_day_across_all_groups(self):
        for _ in range(5):
            public_calendar_text(date(2026,10,27))
        self.assertEqual(public_calendar_text.cache_info().misses,1)
        self.assertEqual(public_calendar_text.cache_info().hits,4)
        self.assertEqual(public_calendar_text.cache_info().maxsize,32)
    def test_navigation_stays_within_three_calendar_days(self):
        now=date(2026,10,29)
        current=day_actions(now,today=now)
        self.assertTrue(any(x=="calendar:2026-10-30" for _,x in current))
        for _,callback in current:
            self.assertLessEqual(len(callback.encode("utf8")),64)
            self.assertEqual(parse_day_callback(callback,today=now).year,2026)
        edge=day_actions(now+__import__("datetime").timedelta(days=NEARBY_DAYS),today=now)
        self.assertFalse(any(x.endswith("2026-11-02") for _,x in edge))
        for raw in ("calendar:2026-11-02","calendar:2026-10-29T11:30","calendar:2005-12-23",
                    "calendar:2026-02-30","calendar:2026-10-29:private", "evidence:test"):
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                parse_day_callback(raw,today=now)
        self.assertFalse(valid_nearby_day(now+__import__("datetime").timedelta(days=4),today=now))
    def test_chats_never_provide_birth_data(self):
        self.assertNotIn("1999-12-31",public_calendar_text(date(2026,10,27)))
        self.assertIsInstance(myanmar_today(),date)
    def test_harden_if_calendar_becomes_personalized(self):
        good={"personalized":True,"prediction_supported":False}
        with patch("public_calendar.daily_calendar_reading",return_value=good):
            public_calendar_text.cache_clear()
            with self.assertRaises(ValueError):
                public_calendar_text(date(2026,10,27))

class GroupGateTests(unittest.TestCase):
    def test_one_message_per_group_without_writes(self):
        now=[100.0]
        g=GroupCalendarGate(seconds=20,capacity=2,clock=lambda:now[0])
        self.assertTrue(g.allow(-123))
        self.assertFalse(g.allow(-123))
        self.assertTrue(g.allow(-987))
        self.assertFalse(g.allow(123))
        now[0]+=20
        self.assertTrue(g.allow(-123))
        self.assertTrue(g.allow(-77))
        self.assertEqual(len(g._seen),2)
    def test_reject_invalid_throttle(self):
        for sec,n in ((0,3),(3,0),(True,3)):
            with self.subTest(sec=sec,n=n),self.assertRaises(ValueError):
                GroupCalendarGate(sec,n)
if __name__=="__main__":
    unittest.main()
