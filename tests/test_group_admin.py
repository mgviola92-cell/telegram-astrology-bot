"""No fake group-admin callback can change another group's settings."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from group_admin import is_verified_group_admin

class TelegramAdminTests(unittest.IsolatedAsyncioTestCase):
    async def test_only_telegram_current_admin_or_owner(self):
        bot=SimpleNamespace(get_chat_member=AsyncMock())
        for status,expected in [("creator",True),("administrator",True),
                                ("member",False),("left",False),
                                ("restricted",False),("kicked",False)]:
            with self.subTest(status=status):
                bot.get_chat_member.return_value=SimpleNamespace(status=status)
                self.assertEqual(await is_verified_group_admin(bot,-101,SimpleNamespace(id=22)),expected)
        self.assertEqual(bot.get_chat_member.await_args.kwargs,{"chat_id":-101,"user_id":22})
    async def test_unknown_id_and_anonymous_sender_deny_without_api_call(self):
        bot=SimpleNamespace(get_chat_member=AsyncMock(return_value=SimpleNamespace(status="administrator")))
        self.assertFalse(await is_verified_group_admin(bot,-101,None))
        self.assertFalse(await is_verified_group_admin(bot,-101,SimpleNamespace(id=0)))
        self.assertFalse(await is_verified_group_admin(bot,-101,SimpleNamespace(id=22),sender_chat=object()))
        self.assertFalse(await is_verified_group_admin(bot,101,SimpleNamespace(id=22)))
        bot.get_chat_member.assert_not_awaited()
    async def test_api_errors_fail_closed_without_leaking(self):
        bot=SimpleNamespace(get_chat_member=AsyncMock(side_effect=RuntimeError("private")))
        self.assertFalse(await is_verified_group_admin(bot,-101,SimpleNamespace(id=22)))

if __name__=="__main__":
    unittest.main()
