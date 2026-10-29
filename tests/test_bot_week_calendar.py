"""Telegram offline integration tests for group/private seven-day calendar."""
import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock,patch
import bot
from group_calendar_settings import GroupCalendarSettings

GROUP=-100766001
TODAY=date(2026,10,29)

def message(kind="supergroup",cmd="/week",chat_id=GROUP):
    return SimpleNamespace(
        text=cmd,chat=SimpleNamespace(type=kind,id=chat_id),answer=AsyncMock())

def callback(data,kind="supergroup",chat_id=GROUP):
    msg=SimpleNamespace(chat=SimpleNamespace(type=kind,id=chat_id),
                        edit_text=AsyncMock(),answer=AsyncMock())
    return SimpleNamespace(data=data,message=msg,answer=AsyncMock())

class WeekCommandTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.settings=GroupCalendarSettings()
        self.patch=patch.object(bot,"group_settings",self.settings)
        self.patch.start()
        bot.group_calendar_gate._seen.pop(GROUP,None)
    def tearDown(self):
        self.patch.stop()
        bot.group_calendar_gate._seen.pop(GROUP,None)

    async def test_group_week_does_not_send_birth_data(self):
        msg=message()
        with patch("bot.myanmar_today",return_value=TODAY):
            await bot.public_week_command(msg)
        msg.answer.assert_awaited_once()
        card=msg.answer.await_args.args[0]
        self.assertIn("ခုနစ်ရက်",card)
        self.assertIn("2026-10-26",card)
        self.assertIn("2026-11-01",card)
        self.assertNotIn("2005-12-23",card)
        self.assertNotIn("\\n",card)
        self.assertLess(len(card),4096)
        self.assertEqual(msg.answer.await_args.kwargs["parse_mode"],"HTML")
        buttons=[b.callback_data for row in msg.answer.await_args.kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertEqual(len(buttons),3)
        self.assertTrue(all(b.startswith("calendarweek:") for b in buttons))

    async def test_group_week_and_today_share_spam_cooldown(self):
        first=message()
        second=message(cmd="/today")
        with patch("bot.myanmar_today",return_value=TODAY):
            await bot.public_week_command(first)
            await bot.public_today_command(second)
        first.answer.assert_awaited_once()
        second.answer.assert_not_awaited()

    async def test_private_week_no_group_throttle(self):
        private=message("private",chat_id=7332)
        with patch("bot.myanmar_today",return_value=TODAY):
            await bot.public_week_command(private)
            await bot.public_week_command(private)
        self.assertEqual(private.answer.await_count,2)

    async def test_disabled_group_cannot_access_new_or_old_week_cards(self):
        self.settings.set_enabled(GROUP,False)
        msg=message()
        with patch("bot.myanmar_today",return_value=TODAY):
            await bot.public_week_command(msg)
        msg.answer.assert_not_awaited()
        menu=callback("group:week")
        old=callback("calendarweek:2026-10-26")
        with patch("bot.Message",SimpleNamespace),patch("bot.myanmar_today",return_value=TODAY):
            await bot.group_home_week(menu)
            await bot.public_week_navigation(old)
        for cb in (menu,old):
            self.assertTrue(cb.answer.await_args.kwargs["show_alert"])
            cb.message.edit_text.assert_not_awaited()

    async def test_stale_week_callback_rejected(self):
        old=callback("calendarweek:2026-10-19")
        with patch("bot.Message",SimpleNamespace),patch("bot.myanmar_today",return_value=date(2026,11,10)):
            await bot.public_week_navigation(old)
        self.assertTrue(old.answer.await_args.kwargs["show_alert"])
        old.message.edit_text.assert_not_awaited()

    async def test_group_navigation_reuses_same_message(self):
        cb=callback("calendarweek:2026-11-02")
        with patch("bot.Message",SimpleNamespace),patch("bot.myanmar_today",return_value=TODAY):
            await bot.public_week_navigation(cb)
        cb.answer.assert_awaited_once()
        cb.message.edit_text.assert_awaited_once()
        cb.message.answer.assert_not_awaited()
        self.assertIn("2026-11-02",cb.message.edit_text.await_args.args[0])
        markup=cb.message.edit_text.await_args.kwargs["reply_markup"]
        self.assertTrue(all(len(b.callback_data.encode("utf8"))<=64
                            for row in markup.inline_keyboard for b in row))

    async def test_group_home_week_button_edits_in_place(self):
        cb=callback("group:week")
        with patch("bot.Message",SimpleNamespace),patch("bot.myanmar_today",return_value=TODAY):
            await bot.group_home_week(cb)
        self.assertIn("2026-10-26",cb.message.edit_text.await_args.args[0])
        cb.message.answer.assert_not_awaited()

    async def test_bad_command_args_do_not_echo_birth_inputs_in_group(self):
        msg=message(cmd="/week 2005-12-23")
        await bot.public_week_command(msg)
        result=msg.answer.await_args.args[0]
        self.assertIn("/week",result)
        self.assertNotIn("2005-12-23",result)

    async def test_channel_and_missing_callback_are_denied(self):
        msg=message(kind="channel")
        await bot.public_week_command(msg)
        msg.answer.assert_not_awaited()
        cb=callback("calendarweek:2026-10-26",kind="channel")
        with patch("bot.Message",SimpleNamespace):
            await bot.public_week_navigation(cb)
        self.assertTrue(cb.answer.await_args.kwargs["show_alert"])
        cb.message.edit_text.assert_not_awaited()
        cb.message=None
        await bot.public_week_navigation(cb)
        self.assertTrue(cb.answer.await_args.kwargs["show_alert"])

if __name__=="__main__":
    unittest.main()
