"""Group landing uses no birth profiles or private navigation."""
import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from bot import welcome, help_message, group_home_calendar, group_welcome_gate

GROUP=-100555666777

def message(kind, cid):
    return SimpleNamespace(chat=SimpleNamespace(type=kind,id=cid),answer=AsyncMock())

class GroupWelcomeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncTearDown(self):
        group_welcome_gate._seen.pop(GROUP,None)
    async def test_group_start_exposes_only_read_only_public_calendar(self):
        m=message("supergroup",GROUP)
        await welcome(m)
        body=m.answer.await_args.args[0]
        self.assertIn("အဖွဲ့ဇာတာခန်း",body)
        self.assertIn("/today",body)
        cb=[b.callback_data for row in m.answer.await_args.kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertEqual(cb,["group:today","group:week","group:settings"])
        self.assertNotIn("ui:feature:profile",str(m.answer.await_args))
        self.assertNotIn("2005-12-23",body)
        await welcome(m)
        self.assertEqual(m.answer.await_count,1)
    async def test_private_start_preserves_full_menu(self):
        m=message("private",123)
        await welcome(m)
        cb=[b.callback_data for row in m.answer.await_args.kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertIn("ui:feature:profile",cb)
        self.assertIn("ui:category:charts",cb)
    async def test_help_is_same_private_safe_group_menu(self):
        m=message("group",GROUP)
        await help_message(m)
        self.assertIn("အဖွဲ့ဇာတာခန်း",m.answer.await_args.args[0])
    async def test_channels_do_not_receive_command_response(self):
        m=message("channel",-10022233)
        await welcome(m)
        m.answer.assert_not_awaited()

class GroupMenuCallbackTests(unittest.IsolatedAsyncioTestCase):
    def callback(self,kind):
        msg=SimpleNamespace(chat=SimpleNamespace(type=kind,id=GROUP),
                            edit_text=AsyncMock(),answer=AsyncMock())
        return SimpleNamespace(message=msg,answer=AsyncMock(),data="group:today")
    async def test_group_button_edits_existing_card(self):
        cb=self.callback("supergroup")
        with patch("bot.Message",SimpleNamespace),patch("bot.myanmar_today",return_value=date(2026,10,29)):
            await group_home_calendar(cb)
        cb.answer.assert_awaited_once()
        cb.message.edit_text.assert_awaited_once()
        cb.message.answer.assert_not_awaited()
        self.assertIn("2026-10-29",cb.message.edit_text.await_args.args[0])
    async def test_private_or_stale_group_button_denied(self):
        for kind in ("private","channel"):
            cb=self.callback(kind)
            with patch("bot.Message",SimpleNamespace):
                await group_home_calendar(cb)
            self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
            cb.message.edit_text.assert_not_awaited()
        cb=self.callback("supergroup")
        cb.message=None
        await group_home_calendar(cb)
        self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))

if __name__=="__main__":
    unittest.main()
