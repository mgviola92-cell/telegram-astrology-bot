"""Study pages, source provenance and native Telegram privacy (offline)."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from study_library import CHAPTERS, chapter, study_chapter_text, study_index_text
from native_ui import study_index_keyboard, study_chapter_keyboard, feature_keyboard
from bot import study_command, study_navigation

class StudyLibraryTests(unittest.TestCase):
    def test_six_real_chapters_with_verified_source_callbacks(self):
        self.assertEqual(set(CHAPTERS),{"calendar","mahabote","bazi","western","numerology","tarot"})
        self.assertIn("မသိမ်း",study_index_text())
        for key in CHAPTERS:
            with self.subTest(key=key):
                data=chapter(key)
                text=study_chapter_text(key)
                self.assertIn(data["title"],text)
                self.assertIn("\n",text)
                self.assertNotIn("\\n",text)
                self.assertLess(len(text),4096)
                rows=study_chapter_keyboard(key).inline_keyboard
                cbs=[b.callback_data for row in rows for b in row]
                self.assertEqual(len([x for x in cbs if x.startswith("evidence:")]),len(data["rules"]))
                self.assertTrue(all(len(x.encode("utf-8"))<=64 for x in cbs))
                self.assertNotIn("2005-12-23",str(rows))
        index=study_index_keyboard()
        cbs=[b.callback_data for row in index.inline_keyboard for b in row]
        self.assertEqual({c for c in cbs if c.startswith("study:")},{"study:"+x for x in CHAPTERS})
        self.assertIn("ui:study",[b.callback_data for row in feature_keyboard("study").inline_keyboard for b in row])
    def test_invalid_chapter_rejected(self):
        with self.assertRaises(ValueError):
            study_chapter_text("unknown")

class StudyTelegramTests(unittest.IsolatedAsyncioTestCase):
    async def test_private_study_command_and_group_guard(self):
        private=SimpleNamespace(chat=SimpleNamespace(type="private"),answer=AsyncMock())
        group=SimpleNamespace(chat=SimpleNamespace(type="supergroup"),answer=AsyncMock())
        await study_command(private)
        self.assertIn("ကျမ်းလေ့လာခန်း",private.answer.await_args.args[0])
        self.assertEqual(private.answer.await_args.kwargs["parse_mode"],"HTML")
        await study_command(group)
        self.assertIn("Private Chat",group.answer.await_args.args[0])
        self.assertNotIn("reply_markup",group.answer.await_args.kwargs)
    async def test_private_callbacks_edit_one_message_instead_of_posting_more(self):
        msg=SimpleNamespace(chat=SimpleNamespace(type="private"),edit_text=AsyncMock(),answer=AsyncMock())
        cb=SimpleNamespace(data="study:mahabote",message=msg,answer=AsyncMock())
        with patch("bot.Message",SimpleNamespace):
            await study_navigation(cb)
        self.assertEqual(msg.edit_text.await_count,1)
        msg.answer.assert_not_awaited()
        self.assertIn("မဟာဘုတ်",msg.edit_text.await_args.args[0])
        cb.answer.assert_awaited_once()
    async def test_stale_or_unknown_callbacks_are_safe(self):
        unknown=SimpleNamespace(data="study:missing",message=None,answer=AsyncMock())
        await study_navigation(unknown)
        self.assertTrue(unknown.answer.await_args.kwargs.get("show_alert"))
        msg=SimpleNamespace(chat=SimpleNamespace(type="private"),edit_text=AsyncMock(),answer=AsyncMock())
        cb=SimpleNamespace(data="study:invalid",message=msg,answer=AsyncMock())
        with patch("bot.Message",SimpleNamespace):
            await study_navigation(cb)
        self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
        msg.edit_text.assert_not_awaited()

if __name__=="__main__":
    unittest.main()
