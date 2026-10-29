"""Offline Telegram test: private school-attributed Numerology command."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from bot import numerology
from evidence_ui import RULES

def message(cmd, kind="private"):
    return SimpleNamespace(text=cmd, chat=SimpleNamespace(type=kind), answer=AsyncMock())

class NumerologyBotTests(unittest.IsolatedAsyncioTestCase):
    async def test_private_result_is_readable_with_two_public_source_buttons(self):
        m=message("/number 2005-12-23")
        await numerology(m)
        m.answer.assert_awaited_once()
        text=m.answer.await_args.args[0]
        self.assertIn("သင့်ဘဝလမ်းကြောင်းကိန်း",text)
        self.assertIn("ရိုးရာအမြင်",text)
        self.assertIn("\n",text)
        self.assertNotIn("\\n",text)
        self.assertLess(len(text),4096)
        buttons=[b for row in m.answer.await_args.kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertEqual(len(buttons),2)
        self.assertTrue(all(b.callback_data.startswith("evidence:") for b in buttons))
        self.assertTrue(all(b.callback_data.partition(":")[2] in RULES for b in buttons))
        self.assertTrue(all("2005-12-23" not in b.callback_data for b in buttons))
        self.assertEqual(m.answer.await_args.kwargs["parse_mode"],"HTML")
    async def test_no_private_birth_data_in_groups(self):
        m=message("/number 2005-12-23","supergroup")
        await numerology(m)
        self.assertNotIn("2005-12-23",m.answer.await_args.args[0])
        self.assertNotIn("reply_markup",m.answer.await_args.kwargs)
    async def test_invalid_dates_and_extras_rejected(self):
        for value in ("/number 2024-02-30","/number 1899-01-01",
                      "/number 2101-01-01","/number 2005-12-23 extra",
                      "/number 2050-12-23"):
            with self.subTest(value=value):
                m=message(value)
                await numerology(m)
                self.assertNotIn("reply_markup",m.answer.await_args.kwargs)

if __name__=="__main__":
    unittest.main()
