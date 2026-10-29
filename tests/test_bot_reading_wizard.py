"""Telegram offline integration: private date/time wizard, no DB or network."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from bot import (reading_inputs, personal_reading_command,
                 private_reading_input_message, cancel_private_reading)
from native_ui import feature_keyboard

UID=918763450

def message(text,kind="private",who=UID):
    return SimpleNamespace(
        text=text,
        chat=SimpleNamespace(type=kind,id=who),
        from_user=SimpleNamespace(id=who),
        answer=AsyncMock()
    )

class ReadingWizardCommandTests(unittest.IsolatedAsyncioTestCase):
    async def asyncTearDown(self):
        reading_inputs.cancel(UID,UID)

    async def test_start_complete_without_clock(self):
        start=message("/reading")
        await personal_reading_command(start)
        self.assertIn("YYYY-MM-DD",start.answer.await_args.args[0])
        self.assertEqual(reading_inputs.step(UID,UID),"date")
        birth=message("2005-12-23")
        await private_reading_input_message(birth)
        self.assertEqual(reading_inputs.step(UID,UID),"time")
        markup=birth.answer.await_args.kwargs["reply_markup"]
        self.assertEqual(markup.inline_keyboard[0][0].callback_data,"ui:reading:skip")
        self.assertNotIn("2005-12-23",str(markup))
        finish=message("မသိပါ")
        await private_reading_input_message(finish)
        text=finish.answer.await_args.args[0]
        self.assertIn("ကိုယ်ပိုင်ရိုးရာဇာတာ",text)
        self.assertIn("Life Path",text)
        self.assertNotIn("\\n",text)
        self.assertLess(len(text),4096)
        self.assertIsNone(reading_inputs.step(UID,UID))
        callbacks=[b.callback_data for row in finish.answer.await_args.kwargs["reply_markup"].inline_keyboard for b in row]
        self.assertTrue(all("2005-12-23" not in c for c in callbacks))

    async def test_invalid_date_and_time_keep_state(self):
        await personal_reading_command(message("/reading"))
        invalid=message("2050-12-23")
        await private_reading_input_message(invalid)
        self.assertEqual(reading_inputs.step(UID,UID),"date")
        await private_reading_input_message(message("2005-12-23"))
        badtime=message("24:00")
        await private_reading_input_message(badtime)
        self.assertEqual(reading_inputs.step(UID,UID),"time")
        done=message("08:37")
        await private_reading_input_message(done)
        self.assertIn("ကိုယ်ပိုင်ရိုးရာဇာတာ",done.answer.await_args.args[0])

    async def test_cancel_and_group_privacy(self):
        await personal_reading_command(message("/reading"))
        stopped=message("/cancel")
        await cancel_private_reading(stopped)
        self.assertIsNone(reading_inputs.step(UID,UID))
        self.assertIn("မသိမ်း",stopped.answer.await_args.args[0])
        group=message("/reading","supergroup")
        await personal_reading_command(group)
        self.assertIn("Private Chat",group.answer.await_args.args[0])
        self.assertIsNone(reading_inputs.step(UID,UID))

    def test_native_start_button_has_no_birth_data(self):
        markup=feature_keyboard("reading")
        cb=[button.callback_data for row in markup.inline_keyboard for button in row]
        self.assertIn("ui:reading:start",cb)
        self.assertIn("ui:guide:reading",cb)
        self.assertTrue(all(len(x.encode("utf-8"))<=64 for x in cb))

if __name__=="__main__":
    unittest.main()
