"""Offline Telegram tests for daily Myanmar calendar classification."""
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from bot import daily_command

def message(command, chat_type="private"):
    return SimpleNamespace(
        text=command, chat=SimpleNamespace(type=chat_type),
        answer=AsyncMock(),
    )

class DailyCommandTests(unittest.IsolatedAsyncioTestCase):
    async def test_documented_october_2026_yatyaza(self):
        m=message("/daily 2026-10-27")
        await daily_command(m)
        m.answer.assert_awaited_once()
        text=m.answer.await_args.args[0]
        self.assertIn("2026-10-27",text)
        self.assertIn("ရက်ရာဇာ",text)
        self.assertNotIn("ကံကြမ္မာသေချာ",text)
        self.assertLess(len(text),4096)
        callbacks=[b.callback_data for row in m.answer.await_args.kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertIn("evidence:MM-CALENDAR-DAY-SIGNALS-001",callbacks)
        self.assertIn("evidence:MM-DAILY-CALENDAR-REFLECTION-001",callbacks)
        self.assertFalse(any("2026-10-27" in x for x in callbacks))

    async def test_todays_local_calendar_day_is_used_without_birth_data(self):
        m=message("/daily")
        await daily_command(m)
        self.assertIn("<b>မြန်မာရိုးရာ",m.answer.await_args.args[0])
        self.assertIn("မြန်မာစံတော်ချိန်",m.answer.await_args.args[0])

    async def test_birth_data_never_accepted_as_command_arguments(self):
        for value in ("/daily 2026-10-28 11:30",
                      "/daily 2026-10-28 Asia/Yangon"):
            m=message(value)
            await daily_command(m)
            self.assertIn("/daily",m.answer.await_args.args[0])
            self.assertNotIn("reply_markup",m.answer.await_args.kwargs)

    async def test_private_chat_only(self):
        m=message("/daily 2026-10-28","supergroup")
        await daily_command(m)
        self.assertIn("Private Chat",m.answer.await_args.args[0])
        self.assertNotIn("reply_markup",m.answer.await_args.kwargs)

    async def test_bad_dates_do_not_produce_result(self):
        for value in ("2026-02-30","1899-01-01","2101-01-01","garbage"):
            m=message("/daily "+value)
            await daily_command(m)
            self.assertIn("YYYY-MM-DD",m.answer.await_args.args[0])
            self.assertNotIn("reply_markup",m.answer.await_args.kwargs)

if __name__=="__main__":
    unittest.main()
