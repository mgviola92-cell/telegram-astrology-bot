"""The native UI should edit in place, not duplicate Telegram messages."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import EditMessageText
from native_message_edit import edit_or_reply
from bot import native_navigation,show_evidence

class EditEfficiencyTests(unittest.IsolatedAsyncioTestCase):
    def msg(self):
        return SimpleNamespace(edit_text=AsyncMock(),answer=AsyncMock())
    async def test_existing_message_edited(self):
        msg=self.msg()
        outcome=await edit_or_reply(msg,"<b>hello</b>")
        self.assertEqual(outcome,"edited")
        msg.answer.assert_not_awaited()
    async def test_unchanged_is_not_an_error_or_duplicate(self):
        msg=self.msg()
        msg.edit_text.side_effect=TelegramBadRequest(
            method=EditMessageText(chat_id=17,message_id=11,text="same"),
            message="Bad Request: message is not modified: specified new message content and reply markup are exactly the same")
        self.assertEqual(await edit_or_reply(msg,"same"),"unchanged")
        msg.answer.assert_not_awaited()
    async def test_failed_edit_falls_back_only_once(self):
        msg=self.msg()
        msg.edit_text.side_effect=ValueError("cannot edit")
        self.assertEqual(await edit_or_reply(msg,"fallback"),"fallback")
        self.assertEqual(msg.answer.await_count,1)

class EvidencePrivacyTests(unittest.IsolatedAsyncioTestCase):
    def msg(self):
        return SimpleNamespace(edit_text=AsyncMock(),answer=AsyncMock())
    def callback(self, kind):
        msg=SimpleNamespace(chat=SimpleNamespace(type=kind),answer=AsyncMock())
        return SimpleNamespace(message=msg,answer=AsyncMock(),
            from_user=SimpleNamespace(id=13),
            data="evidence:MM-MAHABOTE-SEVEN-HOUSE-001")
    async def test_group_button_never_posts_evidence(self):
        cb=self.callback("supergroup")
        with patch("bot.Message",SimpleNamespace):
            await show_evidence(cb)
        self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
        cb.message.answer.assert_not_awaited()
    async def test_private_source_still_accessible(self):
        cb=self.callback("private")
        with patch("bot.Message",SimpleNamespace):
            await show_evidence(cb)
        self.assertIn("တွက်ချက်ပုံ",cb.message.answer.await_args.args[0])
        self.assertEqual(cb.message.answer.await_args.kwargs["parse_mode"],"HTML")
    async def test_native_repeat_navigation_does_not_multiply_cards(self):
        msg=self.msg()
        msg.chat=SimpleNamespace(type="private")
        cb=SimpleNamespace(data="ui:home",message=msg,answer=AsyncMock())
        msg.edit_text.side_effect=TelegramBadRequest(
            method=EditMessageText(chat_id=17,message_id=11,text="same"),
            message="Bad Request: message is not modified")
        with patch("bot.Message",SimpleNamespace):
            await native_navigation(cb)
        msg.answer.assert_not_awaited()
        cb.answer.assert_awaited_once()

if __name__=="__main__":
    unittest.main()
