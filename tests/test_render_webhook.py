"""Render Web Service webhook config and public routes: offline only."""
import unittest
from aiogram import Bot,Dispatcher
from aiohttp.test_utils import TestClient,TestServer
from render_webhook import (
    HEALTH_PATH,WEBHOOK_PATH,webhook_configuration,webhook_application,
)
SECRET="a"*40
BASE={
    "RENDER":"true","RENDER_SERVICE_TYPE":"web",
    "RENDER_EXTERNAL_URL":"https://telegram-astrology-bot.onrender.com",
    "TELEGRAM_WEBHOOK_SECRET":SECRET,
    "PORT":"10000",
}

class ConfigTests(unittest.TestCase):
    def test_render_web_service_settings_and_routes(self):
        conf=webhook_configuration(BASE)
        self.assertEqual(conf["port"],10000)
        self.assertEqual(conf["public_url"],BASE["RENDER_EXTERNAL_URL"])
        self.assertEqual(conf["webhook_url"],BASE["RENDER_EXTERNAL_URL"]+WEBHOOK_PATH)
        self.assertEqual(conf["secret"],SECRET)

    def test_fails_closed_on_missing_or_bad_origin_secret_or_port(self):
        changes=(
            {"RENDER_EXTERNAL_URL":""},
            {"RENDER_EXTERNAL_URL":"http://example.onrender.com"},
            {"RENDER_EXTERNAL_URL":"https://user:pass@example.com"},
            {"RENDER_EXTERNAL_URL":"https://example.onrender.com/else"},
            {"RENDER_EXTERNAL_URL":"https://example.onrender.com?x=1"},
            {"TELEGRAM_WEBHOOK_SECRET":""},
            {"TELEGRAM_WEBHOOK_SECRET":"short"},
            {"TELEGRAM_WEBHOOK_SECRET":"x"*40+"!"},
            {"PORT":"abc"},
            {"PORT":"19099"},
            {"PORT":"65536"},
            {"PORT":"0"},
        )
        for change in changes:
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    webhook_configuration(BASE|change)

    def test_local_polling_fallback(self):
        self.assertIsNone(webhook_configuration({}))
        self.assertIsNone(webhook_configuration({"RENDER_SERVICE_TYPE":"worker"}))

class WebhookRoutesTests(unittest.IsolatedAsyncioTestCase):
    async def test_health_and_webhook_auth_and_no_birth_info(self):
        ready={"registered":False}
        dp=Dispatcher()
        async with Bot(token="123:TEST_BOT") as bot:
            app=webhook_application(dp,bot,webhook_configuration(BASE),ready)
            async with TestServer(app) as server:
                async with TestClient(server) as client:
                    resp=await client.get("/")
                    self.assertEqual(resp.status,200)
                    self.assertNotIn("123:TEST_BOT",await resp.text())
                    resp=await client.get(HEALTH_PATH)
                    self.assertEqual(resp.status,503)
                    ready["registered"]=True
                    resp=await client.get(HEALTH_PATH)
                    self.assertEqual(resp.status,200)
                    self.assertEqual(await resp.text(),"ok\n")
                    bad=await client.post(WEBHOOK_PATH,json={"update_id":1})
                    self.assertIn(bad.status,(401,403))
                    incorrect=await client.post(
                        WEBHOOK_PATH,json={"update_id":1},
                        headers={"X-Telegram-Bot-Api-Secret-Token":"wrong"})
                    self.assertIn(incorrect.status,(401,403))
                    self.assertNotIn("123:TEST_BOT",await incorrect.text())

if __name__=="__main__":
    unittest.main()
