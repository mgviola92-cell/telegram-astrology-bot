import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from bot import profection_command
from evidence_ui import RULES

def make_message(text,chat_type="private"):
    return SimpleNamespace(text=text,chat=SimpleNamespace(type=chat_type),answer=AsyncMock())

class ProfectionCommandTests(unittest.IsolatedAsyncioTestCase):
    async def test_actual_birthday_calculation_and_method(self):
        msg=make_message("/profection 2005-12-23 2026-12-23 Aries")
        await profection_command(msg)
        msg.answer.assert_awaited_once()
        body=msg.answer.await_args.args[0]
        kwargs=msg.answer.await_args.kwargs
        self.assertIn("နှစ်တိုင်အိမ် — <b>10</b>",body)
        self.assertIn("Capricorn",body)
        self.assertIn("Saturn",body)
        self.assertIn("အသုံးပြုသူပေးထားသည်",body)
        self.assertNotIn(chr(92)+"n",body)
        self.assertLess(len(body),4096)
        self.assertEqual(kwargs["reply_markup"].inline_keyboard[0][0].callback_data,
                         "evidence:WEST-HEL-ANNUAL-PROFECTION-001")
        self.assertIn("WEST-HEL-ANNUAL-PROFECTION-001",RULES)

    async def test_house_changes_on_birthday(self):
        before=make_message("/profection 2005-12-23 2026-12-22 Aries")
        after=make_message("/profection 2005-12-23 2026-12-23 Aries")
        await profection_command(before)
        await profection_command(after)
        self.assertIn("နှစ်တိုင်အိမ် — <b>9</b>",before.answer.await_args.args[0])
        self.assertIn("နှစ်တိုင်အိမ် — <b>10</b>",after.answer.await_args.args[0])

    async def test_missing_rising_sign_shows_clear_guide(self):
        msg=make_message("/profection 2005-12-23 2026-10-27")
        await profection_command(msg)
        self.assertIn("Ascendant",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

    async def test_group_birth_date_private_only(self):
        msg=make_message("/profection 2005-12-23 2026-10-27 Aries","supergroup")
        await profection_command(msg)
        self.assertIn("Private Chat",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

    async def test_invalid_rising_sign_fails_closed(self):
        msg=make_message("/profection 2005-12-23 2026-10-27 Unknown")
        await profection_command(msg)
        self.assertIn("Rising Sign",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

if __name__=="__main__":
    unittest.main()
