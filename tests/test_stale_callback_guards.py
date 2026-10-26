import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from bot import native_navigation, show_evidence, tarot_pick

def stale(data):
    return SimpleNamespace(data=data,message=None,answer=AsyncMock())

class StaleCallbackTests(unittest.IsolatedAsyncioTestCase):
    async def test_stale_home_navigation_is_safe(self):
        query=stale("ui:home")
        await native_navigation(query)
        query.answer.assert_awaited_once()
        self.assertTrue(query.answer.await_args.kwargs.get("show_alert"))

    async def test_stale_method_button_is_safe(self):
        query=stale("evidence:MM-MAHABOTE-SEVEN-HOUSE-001")
        await show_evidence(query)
        query.answer.assert_awaited_once()
        self.assertTrue(query.answer.await_args.kwargs.get("show_alert"))

    async def test_stale_tarot_pick_is_not_consumed(self):
        query=stale("tarotpick:missingtoken:0")
        await tarot_pick(query)
        query.answer.assert_awaited_once()
        self.assertTrue(query.answer.await_args.kwargs.get("show_alert"))

if __name__=="__main__":
    unittest.main()
