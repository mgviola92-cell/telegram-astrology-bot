"""Offline Telegram command smoke tests. No bot token and no network."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot import mahabote_command, myanmar_day_signals_command, myday_command
from evidence_ui import RULES


def message(text, chat_type="private"):
    return SimpleNamespace(
        text=text,
        chat=SimpleNamespace(type=chat_type),
        answer=AsyncMock(),
    )

class MyanmarCommandsTests(unittest.IsolatedAsyncioTestCase):
    async def test_myday_birth_weekday_isolated_from_bazi_growth_stages(self):
        msg=message("/myday 2005-12-23 08:37")
        await myday_command(msg)
        msg.answer.assert_awaited_once()
        args,kwargs=msg.answer.await_args
        self.assertIn("မြန်မာ့မွေးနေ့နံ",args[0])
        self.assertNotIn("十二长生",args[0])
        self.assertEqual(kwargs["parse_mode"],"HTML")

    async def test_mahabote_writes_complete_chart(self):
        msg=message("/mahabote 1990-05-14")
        await mahabote_command(msg)
        msg.answer.assert_awaited_once()
        args,kwargs=msg.answer.await_args
        text=args[0]
        self.assertIn("ပုတိ",text)
        self.assertIn("အိမ် ၇ လုံး",text)
        self.assertIn("ဖွားအိမ်၏ ရိုးရာသင်္ကေတအနက်",text)
        self.assertIn("အခြားအိမ်များ၏ သင်္ကေတအညွှန်း",text)
        self.assertIn("★ ပုတိ",text)
        self.assertIn("1990",msg.text)
        self.assertLess(len(text),4096)
        self.assertEqual(kwargs["parse_mode"],"HTML")
        buttons=[b for row in kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertEqual(len(buttons),2)
        self.assertTrue(all(b.callback_data.split(":",1)[1] in RULES for b in buttons))
        self.assertNotIn(chr(92)+"n",text)

    async def test_mahabote_rahu_not_eighth_house(self):
        msg=message("/mahabote 2024-01-03 12:30")
        await mahabote_command(msg)
        msg.answer.assert_awaited_once()
        args,_=msg.answer.await_args
        self.assertIn("ရာဟု",args[0])
        self.assertIn("အိမ် ၇ လုံး",args[0])

    async def test_mahabote_in_group_does_not_display_birth_chart(self):
        msg=message("/mahabote 1990-05-14","supergroup")
        await mahabote_command(msg)
        msg.answer.assert_awaited_once()
        args,_=msg.answer.await_args
        self.assertNotIn("ပုတိ",args[0])
        self.assertIn("သီးသန့်",args[0])

    async def test_day_markers_show_source_verified_golden_date(self):
        msg=message("/days 2024-01-01")
        await myanmar_day_signals_command(msg)
        msg.answer.assert_awaited_once()
        args,kwargs=msg.answer.await_args
        self.assertIn("အမှတ်အသား မတွေ့ပါ",args[0])
        self.assertIn("နဂါးခေါင်းလှည့်ရာ",args[0])
        self.assertIn("တောင်",args[0])
        self.assertEqual(kwargs["parse_mode"],"HTML")
        self.assertEqual(kwargs["reply_markup"].inline_keyboard[0][0].callback_data,
                         "evidence:MM-CALENDAR-DAY-SIGNALS-001")
        self.assertNotIn(chr(92)+"n",args[0])

    async def test_invalid_day_markers_rejected_without_traceback(self):
        msg=message("/days not-a-date")
        await myanmar_day_signals_command(msg)
        msg.answer.assert_awaited_once()
        self.assertIn("YYYY-MM-DD",msg.answer.await_args.args[0])

    async def test_birth_clock_and_date_must_be_canonical_local_values(self):
        for invalid in (
            "/mahabote 2024-01-03 12:30:00",
            "/mahabote 2024-01-03 12:30Z",
            "/mahabote 2024-01-03 8:37",
            "/mahabote 2024-01-03 24:00",
            "/mahabote 2024-01-03T00:00",
            "/mahabote 2100-01-01",
        ):
            with self.subTest(invalid=invalid):
                msg=message(invalid)
                await mahabote_command(msg)
                self.assertIn("YYYY-MM-DD",msg.answer.await_args.args[0])
                self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)
        for valid in ("/mahabote 2024-01-03 11:59",
                      "/mahabote 2024-01-03 12:00"):
            with self.subTest(valid=valid):
                msg=message(valid)
                await mahabote_command(msg)
                self.assertIn("ဗုဒ္ဓဟူး",msg.answer.await_args.args[0])

    async def test_invalid_mahabote_rejected_without_traceback(self):
        msg=message("/mahabote 1700-01-01")
        await mahabote_command(msg)
        msg.answer.assert_awaited_once()
        self.assertIn("1900",msg.answer.await_args.args[0])

if __name__=="__main__":
    unittest.main()
