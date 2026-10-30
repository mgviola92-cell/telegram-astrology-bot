"""Polling startup fail-closed checks: no real bot token or network."""
import os
import unittest
from unittest.mock import AsyncMock,MagicMock,patch
from types import SimpleNamespace
from bot import main

class StartupSafetyTests(unittest.IsolatedAsyncioTestCase):
    async def test_preflight_failure_blocks_telegram_client(self):
        error_report={"passed":False,"checks":[
            {"name":"telegram_token","passed":False},
            {"name":"tarot_manifest_valid","passed":False},
            {"name":"optional:tarot_photo_coverage","passed":True},
        ]}
        with patch.dict(os.environ,{"TELEGRAM_BOT_TOKEN":"123:DO_NOT_PRINT"},clear=True):
            with patch("bot.inspect_environment",return_value=error_report) as preflight:
                with patch("bot.Bot") as constructor:
                    with self.assertRaises(SystemExit) as caught:
                        await main()
        self.assertIn("telegram_token",str(caught.exception))
        self.assertIn("tarot_manifest_valid",str(caught.exception))
        self.assertNotIn("DO_NOT_PRINT",str(caught.exception))
        self.assertNotIn("optional:tarot_photo_coverage",str(caught.exception))
        preflight.assert_called_once_with(mode="deploy")
        constructor.assert_not_called()

    async def test_valid_preflight_allows_only_intended_poll_sequence(self):
        report={"passed":True,"checks":[{"name":"telegram_token","passed":True}]}
        fake=SimpleNamespace(delete_webhook=AsyncMock())
        client=MagicMock()
        client.__aenter__=AsyncMock(return_value=fake)
        client.__aexit__=AsyncMock(return_value=False)
        with patch.dict(os.environ,{"TELEGRAM_BOT_TOKEN":"123:NONLIVE"},clear=True):
            with patch("bot.inspect_environment",return_value=report):
                with patch("bot.Bot",return_value=client) as factory:
                    with patch("bot.dp.start_polling",new_callable=AsyncMock) as poll:
                        await main()
        factory.assert_called_once_with(token="123:NONLIVE")
        fake.delete_webhook.assert_awaited_once_with(drop_pending_updates=False)
        poll.assert_awaited_once_with(fake)
        client.__aexit__.assert_awaited_once()

if __name__=="__main__":
    unittest.main()
