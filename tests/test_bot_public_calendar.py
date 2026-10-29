"""Offline group/private Telegram tests for opt-in, low-cost public calendar."""
import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from bot import (group_calendar_gate, public_calendar_navigation,
                 public_calendar_keyboard, public_today_command)
from public_calendar import public_calendar_text, GroupCalendarGate

def message(text="/today", kind="supergroup", chat_id=-1009876543):
    return SimpleNamespace(
        text=text,
        chat=SimpleNamespace(type=kind,id=chat_id),
        answer=AsyncMock()
    )

class GroupTodayCommandTests(unittest.IsolatedAsyncioTestCase):
    async def asyncTearDown(self):
        group_calendar_gate._seen.pop(-1009876543,None)

    async def test_group_command_on_demand_has_no_private_data_or_db(self):
        m=message()
        with patch("bot.myanmar_today",return_value=date(2026,10,27)):
            await public_today_command(m)
        m.answer.assert_awaited_once()
        content=m.answer.await_args.args[0]
        self.assertIn("2026-10-27",content)
        self.assertIn("မြန်မာရိုးရာ",content)
        self.assertNotIn("2005-12-23",content)
        self.assertIn("မွေးဇာတာ",content)
        self.assertNotIn("\\n",content)
        self.assertLess(len(content),1800)
        keyboard=m.answer.await_args.kwargs["reply_markup"]
        callbacks=[b.callback_data for row in keyboard.inline_keyboard for b in row]
        self.assertTrue(all(x.startswith("calendar:") for x in callbacks))
        self.assertFalse(any("evidence:" in x for x in callbacks))
        self.assertEqual(m.answer.await_args.kwargs["parse_mode"],"HTML")

    async def test_group_duplicate_request_quietly_throttled(self):
        m=message()
        with patch("bot.myanmar_today",return_value=date(2026,10,27)):
            await public_today_command(m)
            await public_today_command(m)
        self.assertEqual(m.answer.await_count,1)
        self.assertEqual(group_calendar_gate._seen.keys(),{-1009876543} | (group_calendar_gate._seen.keys() - {-1009876543}))

    async def test_command_rejects_extra_arguments_and_channel(self):
        m=message("/today 2005-12-23")
        await public_today_command(m)
        self.assertIn("/today",m.answer.await_args.args[0])
        self.assertNotIn("reply_markup",m.answer.await_args.kwargs)
        channel=message(kind="channel",chat_id=-1007777)
        await public_today_command(channel)
        channel.answer.assert_not_awaited()

    async def test_private_today_not_affected_by_group_gate(self):
        m=message(kind="private",chat_id=998)
        with patch("bot.myanmar_today",return_value=date(2026,10,27)):
            await public_today_command(m)
        self.assertIn("2026-10-27",m.answer.await_args.args[0])

class GroupTodayCallbackTests(unittest.IsolatedAsyncioTestCase):
    def callback(self, data, kind="supergroup"):
        msg=SimpleNamespace(
            chat=SimpleNamespace(id=-10012345,type=kind),
            edit_text=AsyncMock(),answer=AsyncMock(),
        )
        return SimpleNamespace(data=data,message=msg,answer=AsyncMock())

    async def test_group_navigation_edits_original_message(self):
        cb=self.callback("calendar:2026-10-28")
        with patch("bot.Message",SimpleNamespace),patch("bot.myanmar_today",return_value=date(2026,10,29)):
            await public_calendar_navigation(cb)
        cb.answer.assert_awaited_once()
        self.assertEqual(cb.message.edit_text.await_count,1)
        cb.message.answer.assert_not_awaited()
        self.assertIn("2026-10-28",cb.message.edit_text.await_args.args[0])

    async def test_invalid_and_stale_callback_are_denied_without_edit(self):
        for data in ("calendar:2027-01-01","calendar:2005-12-23",
                     "calendar:broken","calendar:2026-10-29:extra"):
            with self.subTest(data=data):
                cb=self.callback(data)
                with patch("bot.Message",SimpleNamespace),patch("bot.myanmar_today",return_value=date(2026,10,29)):
                    await public_calendar_navigation(cb)
                self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
                cb.message.edit_text.assert_not_awaited()
                cb.message.answer.assert_not_awaited()

    async def test_stale_or_channel_callback_denied(self):
        cb=self.callback("calendar:2026-10-29")
        cb.message=None
        await public_calendar_navigation(cb)
        self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
        ch=self.callback("calendar:2026-10-29",kind="channel")
        with patch("bot.Message",SimpleNamespace):
            await public_calendar_navigation(ch)
        self.assertTrue(ch.answer.await_args.kwargs.get("show_alert"))
        ch.message.edit_text.assert_not_awaited()

    def test_navigation_callback_is_public_only(self):
        buttons=public_calendar_keyboard(date(2026,10,29),today=date(2026,10,29))
        self.assertTrue(all(len(b.callback_data.encode())<=64
                            for row in buttons.inline_keyboard for b in row))

if __name__=="__main__":
    unittest.main()
