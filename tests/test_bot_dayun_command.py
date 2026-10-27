import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from bot import dayun_command
from evidence_ui import RULES

def message(text,chat_type="private"):
    return SimpleNamespace(
        text=text,
        chat=SimpleNamespace(type=chat_type),
        answer=AsyncMock(),
    )

class DaYunBotCommandTests(unittest.IsolatedAsyncioTestCase):
    async def test_valid_source_calculated_cycles(self):
        msg=message("/dayun 2005-12-23 08:37 Asia/Yangon 1")
        await dayun_command(msg)
        msg.answer.assert_awaited_once()
        args,kwargs=msg.answer.await_args
        body=args[0]
        self.assertIn("大运",body)
        self.assertIn("Asia/Yangon",body)
        self.assertIn("nominal age",body)
        self.assertNotIn(chr(92)+"n",body)
        self.assertLess(len(body),4096)
        markup=kwargs["reply_markup"]
        cb=markup.inline_keyboard[0][0].callback_data
        self.assertEqual(cb,"evidence:CHN-BAZI-DAYUN-001")
        self.assertIn(cb.split(":",1)[1],RULES)

    async def test_both_explicit_method_codes(self):
        for code in ("0","1"):
            with self.subTest(code=code):
                msg=message("/dayun 2005-12-23 08:37 Asia/Yangon "+code)
                await dayun_command(msg)
                self.assertIn("BaZi",msg.answer.await_args.args[0])

    async def test_sect_choice_allowed(self):
        msg=message("/dayun 2005-12-23 08:37 Asia/Yangon 0 2")
        await dayun_command(msg)
        self.assertIn("Yun Sect — 2",msg.answer.await_args.args[0])

    async def test_missing_code_requires_explicit_selection(self):
        msg=message("/dayun 2005-12-23 08:37 Asia/Yangon")
        await dayun_command(msg)
        self.assertIn("Code 1",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

    async def test_group_birth_data_never_rendered(self):
        msg=message("/dayun 2005-12-23 08:37 Asia/Yangon 1","supergroup")
        await dayun_command(msg)
        self.assertIn("Private Chat",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

    async def test_dst_fall_overlap_fails_closed(self):
        msg=message("/dayun 2024-11-03 01:30 America/New_York 1")
        await dayun_command(msg)
        self.assertIn("DST",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

    async def test_invalid_code_rejected(self):
        msg=message("/dayun 2005-12-23 08:37 Asia/Yangon 3")
        await dayun_command(msg)
        self.assertIn("Code 1",msg.answer.await_args.args[0])

if __name__=="__main__":
    unittest.main()
