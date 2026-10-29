import unittest
from datetime import date, time
from types import SimpleNamespace
from unittest.mock import AsyncMock
from astro_core import life_path
from mahabote_core import calculate_mahabote
from personal_reading import personal_reading
from bot import personal_reading_command

class PersonalReadingTests(unittest.TestCase):
    def test_no_cross_tradition_invention_and_exact_calculations(self):
        for day in (date(1990,5,14),date(2005,12,23),date(2024,1,3)):
            with self.subTest(day=day):
                reading=personal_reading(day)
                self.assertEqual(reading["life_path"],life_path(day)["number"])
                self.assertEqual(reading["house"],calculate_mahabote(day)["house_burmese"])
                self.assertEqual(reading["synthesis_status"],"parallel_methods_no_predictive_combination")
                self.assertFalse(reading["prediction_supported"])
                self.assertFalse(reading["profile_saved"])
                self.assertEqual(len(reading["evidence_rule_ids"]),4)
                self.assertTrue(reading["life_path_theme"])
                self.assertTrue(reading["life_path_interpretation"])
    def test_wednesday_afternoon_uses_separate_rahu_label(self):
        x=personal_reading(date(2024,1,3),time(13,30))
        self.assertIn("ရာဟု",x["weekday"])
        self.assertEqual(x["house"],personal_reading(date(2024,1,3),time(9,0))["house"])
    def test_inputs_are_bounded(self):
        for bad in (date(1890,1,1),date(2101,1,1),"2005-12-23"):
            with self.assertRaises((TypeError,ValueError)):
                personal_reading(bad)
        with self.assertRaises(ValueError):
            personal_reading(date(2005,12,23),time(8,37,tzinfo=__import__("datetime").timezone.utc))

class PersonalReadingCommandTests(unittest.IsolatedAsyncioTestCase):
    def msg(self,command,chat="private"):
        return SimpleNamespace(text=command,chat=SimpleNamespace(type=chat,id=654321),from_user=SimpleNamespace(id=654321),answer=AsyncMock())
    async def test_private_uses_four_provenance_buttons(self):
        m=self.msg("/reading 2005-12-23 08:37")
        await personal_reading_command(m)
        text=m.answer.await_args.args[0]
        self.assertIn("ကိုယ်ပိုင်ရိုးရာဇာတာ",text)
        self.assertIn("Life Path",text)
        self.assertIn("\n",text)
        self.assertNotIn("\\n",text)
        markup=m.answer.await_args.kwargs["reply_markup"]
        callbacks=[button.callback_data for row in markup.inline_keyboard for button in row]
        self.assertEqual(len(callbacks),4)
        self.assertIn('evidence:NUM-LIFE-PATH-THEMES-001',callbacks)
        self.assertIn('Numerology — Life Path',text)
        self.assertIn('ရိုးရာစနစ်နှစ်ခု',text)
        self.assertTrue(all(c.startswith("evidence:") for c in callbacks))
        self.assertTrue(all("2005-12-23" not in c for c in callbacks))
        self.assertLess(len(text),4096)
    async def test_no_private_birth_data_in_groups(self):
        m=self.msg("/reading 2005-12-23","supergroup")
        await personal_reading_command(m)
        self.assertIn("Private Chat",m.answer.await_args.args[0])
        self.assertNotIn("reply_markup",m.answer.await_args.kwargs)
    async def test_invalid_date_or_time_is_safe(self):
        for command in ("/reading 2101-01-01","/reading 2024-02-30",
                        "/reading 2005-12-23 8:37","/reading 2005-12-23 08:37 extra"):
            with self.subTest(command=command):
                m=self.msg(command)
                await personal_reading_command(m)
                self.assertNotIn("reply_markup",m.answer.await_args.kwargs)

if __name__=="__main__":
    unittest.main()
