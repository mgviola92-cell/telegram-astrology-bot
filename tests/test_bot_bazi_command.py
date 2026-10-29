import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from bot import bazi
from evidence_ui import RULES

def make_message(text,kind="private"):
    return SimpleNamespace(text=text,chat=SimpleNamespace(type=kind),answer=AsyncMock())

class BaziBotCommandTests(unittest.IsolatedAsyncioTestCase):
    async def test_bazi_card_includes_verified_growth_stages(self):
        msg=make_message("/bazi 2005-12-23 08:37 Asia/Yangon")
        await bazi(msg)
        msg.answer.assert_awaited_once()
        args,kwargs=msg.answer.await_args
        body=args[0]
        self.assertIn("乙酉",body)
        self.assertIn("十二长生",body)
        self.assertIn("Ten Gods",body)
        self.assertIn("ရိုးရာ ဓာတ်ဆက်နွယ်မှု ၅ အုပ်စု",body)
        self.assertIn("正印",body)
        self.assertIn("偏财",body)
        self.assertIn("Hidden Stems များကို အလေးချိန်မသတ်မှတ်ရသေး",body)
        self.assertLess(len(body),4096)
        self.assertIn("Solar-Term",body)
        self.assertIn("Winter",body)
        self.assertIn("Asia/Yangon",body)
        self.assertNotIn(chr(92)+"n",body)
        markup=kwargs["reply_markup"]
        self.assertEqual([len(row) for row in markup.inline_keyboard],[2,2,2,1])
        buttons=[b for row in markup.inline_keyboard for b in row]
        self.assertEqual(len({b.text for b in buttons}),7)
        self.assertIn("evidence:CHN-BAZI-TENGODS-SYMBOLIC-001",
                      [b.callback_data for b in buttons])
        self.assertTrue(all("2005-12-23" not in b.callback_data
                            for b in buttons))
        self.assertEqual(set(b.callback_data.split(":",1)[1] for b in buttons)&set(RULES),
                         {b.callback_data.split(":",1)[1] for b in buttons})
        self.assertFalse(any(ord(c)>0x1F000 for b in buttons for c in b.text))

    async def test_group_birth_data_is_not_processed(self):
        msg=make_message("/bazi 2005-12-23 08:37 Asia/Yangon","supergroup")
        await bazi(msg)
        msg.answer.assert_awaited_once()
        args,kwargs=msg.answer.await_args
        self.assertNotIn("乙酉",args[0])
        self.assertNotIn("reply_markup",kwargs)

    async def test_dst_overlap_requires_disambiguation(self):
        msg=make_message("/bazi 2024-11-03 01:30 America/New_York")
        await bazi(msg)
        msg.answer.assert_awaited_once()
        self.assertIn("DST",msg.answer.await_args.args[0])

if __name__=="__main__":
    unittest.main()
