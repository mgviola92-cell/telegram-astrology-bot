"""Offline Telegram integration checks for group /settings admin controls.

Verify group isolation, authorization, stale toggles, group menu, /today,
public card callbacks, and no profile or media data flows.
"""
import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import bot
from group_calendar_settings import GroupCalendarSettings

A=-10099001122
B=-10099002233
ADMIN=10132
MEMBER=88155

def make_bot(status="administrator", failing=False):
    return SimpleNamespace(get_chat_member=AsyncMock(
        side_effect=RuntimeError("verification unavailable") if failing else None,
        return_value=SimpleNamespace(status=status)))

def message(chat=A,who=ADMIN,kind="supergroup",cmd="/settings",status="administrator"):
    return SimpleNamespace(
        text=cmd,chat=SimpleNamespace(id=chat,type=kind),
        from_user=SimpleNamespace(id=who),sender_chat=None,
        bot=make_bot(status),answer=AsyncMock())

def callback(data,chat=A,who=ADMIN,kind="supergroup",status="administrator",msgid=77):
    target=SimpleNamespace(
        chat=SimpleNamespace(id=chat,type=kind),
        message_id=msgid,answer=AsyncMock(),edit_text=AsyncMock())
    return SimpleNamespace(data=data,message=target,bot=make_bot(status),
                           from_user=SimpleNamespace(id=who),answer=AsyncMock())

class GroupSettingsIntegrationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.settings=GroupCalendarSettings()
        self.override=patch.object(bot,"group_settings",self.settings)
        self.override.start()
    def tearDown(self):
        self.override.stop()

    async def test_admin_can_open_settings_and_toggle_group_only(self):
        msg=message()
        await bot.group_settings_command(msg)
        self.assertIn("ဖွင့်ထား",msg.answer.await_args.args[0])
        self.assertIn("ယာယီ",msg.answer.await_args.args[0])
        cb=callback("groupcfg:off")
        with patch("bot.Message",SimpleNamespace):
            await bot.group_settings_navigation(cb)
        self.assertFalse(self.settings.enabled(A))
        self.assertTrue(self.settings.enabled(B))
        self.assertIn("ပိတ်ထား",cb.message.edit_text.await_args.args[0])
        calls=[b.callback_data for row in cb.message.edit_text.await_args.kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertIn("groupcfg:on",calls)
        self.assertNotIn("groupcfg:off",calls)
        self.assertEqual(cb.bot.get_chat_member.await_args.kwargs,{"chat_id":A,"user_id":ADMIN})
        other_group=callback("groupcfg:off",chat=B)
        with patch("bot.Message",SimpleNamespace):
            await bot.group_settings_navigation(other_group)
        self.assertFalse(self.settings.enabled(B))

    async def test_no_user_can_toggle_unless_current_admin(self):
        for status in ("member","left","restricted","kicked"):
            cb=callback("groupcfg:off",status=status)
            with patch("bot.Message",SimpleNamespace):
                await bot.group_settings_navigation(cb)
            self.assertTrue(cb.answer.await_args.kwargs["show_alert"])
            self.assertTrue(self.settings.enabled(A))
            cb.message.edit_text.assert_not_awaited()
        group_message=message(who=MEMBER,status="member")
        await bot.group_settings_command(group_message)
        group_message.answer.assert_not_awaited()

    async def test_telegram_verification_error_fails_closed(self):
        cb=callback("groupcfg:off")
        cb.bot=make_bot(failing=True)
        with patch("bot.Message",SimpleNamespace):
            await bot.group_settings_navigation(cb)
        self.assertTrue(cb.answer.await_args.kwargs["show_alert"])
        self.assertTrue(self.settings.enabled(A))

    async def test_old_inline_toggle_is_not_reapplied(self):
        cb=callback("groupcfg:off")
        with patch("bot.Message",SimpleNamespace):
            await bot.group_settings_navigation(cb)
        old=callback("groupcfg:off")
        with patch("bot.Message",SimpleNamespace):
            await bot.group_settings_navigation(old)
        self.assertFalse(self.settings.enabled(A))
        self.assertIn("ဟောင်း",old.answer.await_args.args[0])
        reenable=callback("groupcfg:on")
        with patch("bot.Message",SimpleNamespace):
            await bot.group_settings_navigation(reenable)
        self.assertTrue(self.settings.enabled(A))

    async def test_disabled_group_silent_even_with_invalid_today_arguments(self):
        self.settings.set_enabled(A,False)
        msg=message(cmd="/today 2005-12-23")
        await bot.public_today_command(msg)
        msg.answer.assert_not_awaited()

    async def test_disabled_group_cannot_use_today_command_or_stale_buttons(self):
        self.settings.set_enabled(A,False)
        m=message(cmd="/today")
        await bot.public_today_command(m)
        m.answer.assert_not_awaited()
        cb=callback("group:today")
        with patch("bot.Message",SimpleNamespace):
            await bot.group_home_calendar(cb)
        self.assertTrue(cb.answer.await_args.kwargs["show_alert"])
        cb.message.edit_text.assert_not_awaited()
        old=callback("calendar:2026-10-29")
        with patch("bot.Message",SimpleNamespace),patch("bot.myanmar_today",return_value=date(2026,10,29)):
            await bot.public_calendar_navigation(old)
        self.assertTrue(old.answer.await_args.kwargs["show_alert"])
        old.message.edit_text.assert_not_awaited()

    async def test_disabled_group_start_hides_calendar_button(self):
        self.settings.set_enabled(A,False)
        m=message(cmd="/start")
        bot.group_welcome_gate._seen.pop(A,None)
        try:
            await bot.welcome(m)
            callbacks=[b.callback_data for row in m.answer.await_args.kwargs["reply_markup"].inline_keyboard for b in row]
            self.assertEqual(callbacks,["group:settings"])
            self.assertNotIn("group:week",callbacks)
            self.assertIn("ပိတ်",m.answer.await_args.args[0])
        finally:
            bot.group_welcome_gate._seen.pop(A,None)

    async def test_private_today_remains_enabled_when_group_disabled(self):
        self.settings.set_enabled(A,False)
        m=message(chat=44,kind="private",cmd="/today")
        with patch("bot.myanmar_today",return_value=date(2026,10,29)):
            await bot.public_today_command(m)
        self.assertIn("2026-10-29",m.answer.await_args.args[0])

    async def test_group_settings_private_callback_blocked(self):
        cb=callback("groupcfg:off",kind="private",chat=44)
        with patch("bot.Message",SimpleNamespace):
            await bot.group_settings_navigation(cb)
        self.assertTrue(cb.answer.await_args.kwargs["show_alert"])
        cb.bot.get_chat_member.assert_not_awaited()
        self.assertTrue(self.settings.enabled(A))

if __name__=="__main__":
    unittest.main()
