import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from aiogram.types import Message
from reference_library import CATEGORY_PREFIXES, library_page, render_library
from bot import reference_category_keyboard, reference_page_keyboard, reference_library_navigation, native_navigation

class ReferenceLibraryTests(unittest.TestCase):
    def test_every_category_covers_each_record_once(self):
        for category in CATEGORY_PREFIXES:
            first=library_page(category,0)
            names=[]
            for index in range(first["page_count"]):
                names.extend(x["id"] for x in library_page(category,index)["items"])
            self.assertEqual(len(names),first["total"])
            self.assertEqual(len(set(names)),len(names))
            for item in names:
                self.assertTrue(item.startswith(CATEGORY_PREFIXES[category]))
    def test_invalid_category_page_and_injection(self):
        for category,page in (("unknown",0),("mm",-1),("mm",100),("mm",1.3)):
            with self.assertRaises(ValueError):
                library_page(category,page)
    def test_render_and_callback_safety(self):
        for category in CATEGORY_PREFIXES:
            info=library_page(category,0)
            content=render_library(info)
            self.assertIn("ကျမ်းကိုးမှတ်တမ်း",content)
            self.assertLess(len(content),4096)
            buttons=reference_page_keyboard(info)
            for row in buttons.inline_keyboard:
                for button in row:
                    self.assertLessEqual(len(button.callback_data.encode()),64)
                    self.assertNotIn("2005-12-23",button.callback_data)
    def test_category_buttons_are_small_and_private(self):
        buttons=reference_category_keyboard()
        self.assertEqual(len(buttons.inline_keyboard),len(CATEGORY_PREFIXES)+1)
        self.assertEqual(buttons.inline_keyboard[0][0].callback_data,"library:mm:0")

class ReferenceLibraryHandlerTests(unittest.IsolatedAsyncioTestCase):
    def fake(self,data,chat_type="private",valid=True):
        message=SimpleNamespace(chat=SimpleNamespace(type=chat_type),
                                edit_text=AsyncMock(),answer=AsyncMock()) if valid else None
        return SimpleNamespace(data=data,message=message,answer=AsyncMock())

    async def test_page_rejects_missing_message(self):
        cb=self.fake("library:mm:0",valid=False)
        await reference_library_navigation(cb)
        self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
    async def test_page_rejects_groups(self):
        cb=self.fake("library:mm:0",chat_type="supergroup")
        await reference_library_navigation(cb)
        self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
    async def test_page_rejects_bad_callbacks(self):
        for value in ("library:invalid:0","library:mm:-1","library:mm:999","library:mm:0:extra"):
            cb=self.fake(value)
            with self.subTest(value=value):
                # Build a real Message for the strict aiogram isinstance guard.
                from aiogram.types import Chat
                cb.message=Message(message_id=1,date=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
                    chat=Chat(id=1,type="private"),text="test")
                await reference_library_navigation(cb)
                self.assertTrue(cb.answer.await_args.kwargs.get("show_alert"))
    async def test_home_route_accepts_library_landing(self):
        from aiogram.types import Chat
        cb=self.fake("ui:library")
        cb.message=Message(message_id=1,date=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
            chat=Chat(id=1,type="private"),text="test")
        # aiogram's Message methods are mocked at class level to avoid Telegram network.
        with unittest.mock.patch.object(Message,"edit_text",new_callable=AsyncMock) as edit:
            await native_navigation(cb)
            self.assertIn("ကျမ်းကိုးမှတ်တမ်း",edit.await_args.args[0])
            self.assertEqual(edit.await_args.kwargs["parse_mode"],"HTML")

if __name__=="__main__":unittest.main()
