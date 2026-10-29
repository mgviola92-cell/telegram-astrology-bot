"""Stop repeat Tarot media requests without DB or sleep tasks."""
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from outbound_budget import CooldownBudget
from bot import tarot_cooldown,open_tarot

class BudgetTests(unittest.TestCase):
    def test_same_owner_cooldown_and_different_owner_isolated(self):
        now=[10.0]
        gate=CooldownBudget(seconds=3,clock=lambda:now[0])
        self.assertTrue(gate.allow(1,10))
        self.assertFalse(gate.allow(1,10))
        self.assertTrue(gate.allow(1,11))
        self.assertTrue(gate.allow(2,10))
        now[0]+=3.0
        self.assertTrue(gate.allow(1,10))
    def test_fixed_capacity_and_reject_invalid(self):
        g=CooldownBudget(capacity=2)
        self.assertFalse(g.allow(0,1))
        self.assertFalse(g.allow(1,True))
        self.assertTrue(g.allow(1,1))
        self.assertTrue(g.allow(1,2))
        self.assertTrue(g.allow(1,3))
        self.assertLessEqual(len(g._latest),2)

class TarotBandwidthTests(unittest.IsolatedAsyncioTestCase):
    async def test_repeated_tarot_request_does_not_send_duplicate_card(self):
        user=871240977
        chat=user
        message=SimpleNamespace(chat=SimpleNamespace(type="private",id=chat),
            answer=AsyncMock(return_value=SimpleNamespace(message_id=7)),
            answer_animation=AsyncMock())
        try:
            with patch.dict(os.environ,{"TAROT_MEDIA_MODE":"text"}):
                await open_tarot(message,user_id=user)
                await open_tarot(message,user_id=user)
            self.assertEqual(message.answer.await_count,1)
            message.answer_animation.assert_not_awaited()
        finally:
            tarot_cooldown._latest.pop((chat,user),None)
    async def test_other_chat_guard(self):
        m=SimpleNamespace(chat=SimpleNamespace(type="supergroup",id=456),
                          answer=AsyncMock(), answer_animation=AsyncMock())
        await open_tarot(m,user_id=123)
        self.assertNotIn((456,123),tarot_cooldown._latest)
        m.answer_animation.assert_not_awaited()

if __name__=="__main__":
    unittest.main()
