"""Native compatibility commands and callback safety, no Telegram network."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock,patch
from bot import compatibility_command,compatibility_navigation,native_navigation
from evidence_ui import RULES
from native_ui import FEATURES,feature_keyboard

def message(text,kind="private"):
    return SimpleNamespace(text=text,chat=SimpleNamespace(type=kind),answer=AsyncMock())

def callback(data,kind="private"):
    return SimpleNamespace(
        data=data,
        message=SimpleNamespace(chat=SimpleNamespace(type=kind),edit_text=AsyncMock()),
        answer=AsyncMock(),
        from_user=SimpleNamespace(id=1234),
    )

class CompatibilityTelegramTests(unittest.IsolatedAsyncioTestCase):
    async def test_private_slash_command_shows_native_12_animal_picker(self):
        m=message("/compat")
        await compatibility_command(m)
        m.answer.assert_awaited_once()
        args,kwargs=m.answer.await_args
        self.assertIn("အကိုင်းသင်္ကေတ",args[0])
        self.assertEqual(kwargs["parse_mode"],"HTML")
        keyboard=kwargs["reply_markup"]
        callbacks=[b.callback_data for row in keyboard.inline_keyboard for b in row]
        self.assertEqual(len([x for x in callbacks if x.startswith("compat:a:")]),12)
        self.assertTrue(all(len(x.encode("utf8"))<=64 for x in callbacks))
        self.assertTrue(all("2005-12-23" not in x for x in callbacks))

    async def test_direct_pair_with_source_link_and_no_birth_data(self):
        m=message("/compat 子 丑")
        await compatibility_command(m)
        m.answer.assert_awaited_once()
        body=m.answer.await_args.args[0]
        kwargs=m.answer.await_args.kwargs
        self.assertIn("六合",body)
        self.assertIn("ကြွက်",body)
        self.assertIn("နွား",body)
        self.assertNotIn("2005",body)
        self.assertIn("မသိမ်း",body)
        self.assertEqual(kwargs["parse_mode"],"HTML")
        callbacks=[b.callback_data for row in kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertIn("compat:start",callbacks)
        self.assertIn("evidence:CHN-BAZI-EARTHLY-BRANCH-PAIR-001",callbacks)
        self.assertIn("CHN-BAZI-EARTHLY-BRANCH-PAIR-001",RULES)

    async def test_group_commands_do_not_generate_pair_result_or_picker(self):
        for input_text in ("/compat","/compat 子 丑"):
            with self.subTest(text=input_text):
                m=message(input_text,"supergroup")
                await compatibility_command(m)
                self.assertIn("Private Chat",m.answer.await_args.args[0])
                self.assertNotIn("reply_markup",m.answer.await_args.kwargs)

    async def test_invalid_commands_no_markup(self):
        for invalid in ("/compat nonsense","/compat 子 x","/compat 子 丑 辰",
                        "/compat <script> 丑","/compat 子子 子"):
            with self.subTest(invalid=invalid):
                m=message(invalid)
                await compatibility_command(m)
                self.assertNotIn("reply_markup",m.answer.await_args.kwargs)

    async def test_staged_callbacks_edit_same_telegram_message(self):
        for data,phrase,count in (
            ("compat:start","ပထမ အကိုင်း",12),
            ("compat:a:子","ဒုတိယ အကိုင်း",12),
            ("compat:b:子:丑","六合",0),
        ):
            with self.subTest(data=data):
                cb=callback(data)
                with patch("bot.Message",SimpleNamespace),patch("bot.edit_or_reply",new_callable=AsyncMock) as edit:
                    await compatibility_navigation(cb)
                cb.answer.assert_awaited_once()
                edit.assert_awaited_once()
                args=edit.await_args.args
                self.assertIn(phrase,args[1])
                buttons=[b.callback_data for row in args[2].inline_keyboard for b in row]
                prefix="compat:b:" if data.startswith("compat:a:") else "compat:a:"
                self.assertEqual(len([x for x in buttons if x.startswith(prefix)]),count)
                self.assertTrue(all("2005" not in code for code in buttons))

    async def test_invalid_and_group_callback_fail_closed(self):
        cases=(("compat:b:子:<", "private"),
               ("compat:a:x","private"),
               ("compat:b:子","private"),
               ("compat:b:子:丑:extra","private"),
               ("compat:start","supergroup"),
               ("compat:b:子:丑","group"))
        for data,chat in cases:
            with self.subTest(data=data,chat=chat):
                cb=callback(data,chat)
                with patch("bot.Message",SimpleNamespace),patch("bot.edit_or_reply",new_callable=AsyncMock) as edit:
                    await compatibility_navigation(cb)
                self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
                edit.assert_not_awaited()

    async def test_native_feature_entry_to_branch_picker(self):
        buttons=[b.callback_data for row in feature_keyboard("compatibility").inline_keyboard for b in row]
        self.assertIn("ui:compat:start",buttons)
        self.assertNotIn("ui:guide:compat",buttons)
        self.assertTrue(FEATURES["compatibility"][2])
        cb=callback("ui:compat:start")
        with patch("bot.Message",SimpleNamespace),patch("bot.edit_or_reply",new_callable=AsyncMock) as edit:
            await native_navigation(cb)
        edit.assert_awaited_once()
        self.assertIn("ပထမ အကိုင်း",edit.await_args.args[1])
        cb.answer.assert_awaited_once()

if __name__=="__main__":
    unittest.main()
