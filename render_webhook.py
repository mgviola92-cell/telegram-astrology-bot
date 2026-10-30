"""Render Web Service Telegram webhook transport.

Use the Render-provided RENDER_EXTERNAL_URL, never guess a hostname.
Secret-header validation is delegated to aiogram's SimpleRequestHandler.
No polling is started in Web Service mode. GET /healthz is public and
only reports webhook registration, never secrets or user information.
"""
import asyncio
import re
import signal
from urllib.parse import urlsplit

WEBHOOK_PATH="/telegram/webhook"
HEALTH_PATH="/healthz"
SECRET_RE=re.compile(r"[A-Za-z0-9_-]{32,256}\Z")

def webhook_configuration(environ):
    """Validate the public HTTPS address, fixed route, port and secret.

    Return None for non-Web Service local/worker polling environments.
    """
    url=environ.get("RENDER_EXTERNAL_URL","").strip()
    if not url:
        if environ.get("RENDER_SERVICE_TYPE","")=="web":
            raise ValueError("Render web service must provide RENDER_EXTERNAL_URL")
        return None
    parsed=urlsplit(url)
    if (parsed.scheme!="https" or not parsed.hostname
            or parsed.username is not None or parsed.password is not None
            or parsed.path not in ("","/") or parsed.query or parsed.fragment
            or parsed.port not in (None,443)):
        raise ValueError("Render external URL must be a bare HTTPS origin")
    secret=environ.get("TELEGRAM_WEBHOOK_SECRET","").strip()
    if not SECRET_RE.fullmatch(secret):
        raise ValueError("TELEGRAM_WEBHOOK_SECRET must contain 32–256 URL-safe random characters")
    raw_port=environ.get("PORT","10000")
    if not raw_port.isascii() or not raw_port.isdecimal():
        raise ValueError("Invalid Render PORT")
    port=int(raw_port)
    if not (1<=port<=65535) or port in (18012,18013,19099):
        raise ValueError("Invalid or reserved Render PORT")
    return {"public_url":f"https://{parsed.netloc}".rstrip("/"),
            "secret":secret,"port":port,
            "webhook_url":f"https://{parsed.netloc}{WEBHOOK_PATH}"}

def webhook_application(dispatcher,bot,config,ready):
    """Construct native aiogram aiohttp adapter for secure webhook requests."""
    from aiohttp import web
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler,setup_application

    app=web.Application(client_max_size=1024*1024)
    async def index(_request):
        return web.Response(text="Telegram astrology service\n")
    async def health(_request):
        if ready["registered"]:
            return web.Response(text="ok\n")
        return web.Response(status=503,text="starting\n")
    app.router.add_get("/",index)
    app.router.add_get(HEALTH_PATH,health)
    SimpleRequestHandler(
        dispatcher=dispatcher,bot=bot,
        secret_token=config["secret"],
        handle_in_background=False,
    ).register(app,path=WEBHOOK_PATH)
    setup_application(app,dispatcher,bot=bot)
    return app

async def run_render_webhook(bot,dispatcher,config):
    """Bind Render PORT and set the Telegram webhook after HTTP startup."""
    from aiohttp import web
    ready={"registered":False}
    app=webhook_application(dispatcher,bot,config,ready)
    runner=web.AppRunner(app,access_log=None)
    await runner.setup()
    stop=asyncio.Event()
    loop=asyncio.get_running_loop()
    installed=[]
    try:
        for sig in (signal.SIGTERM,signal.SIGINT):
            try:
                loop.add_signal_handler(sig,stop.set)
                installed.append(sig)
            except (NotImplementedError,RuntimeError,ValueError):
                pass
        await web.TCPSite(runner,host="0.0.0.0",port=config["port"]).start()
        confirmed=await bot.set_webhook(
            config["webhook_url"],
            secret_token=config["secret"],
            drop_pending_updates=False,
            allowed_updates=dispatcher.resolve_used_update_types(),
            max_connections=1,
        )
        if confirmed is not True:
            raise RuntimeError("Telegram did not confirm webhook registration")
        ready["registered"]=True
        await stop.wait()
    finally:
        ready["registered"]=False
        for sig in installed:
            loop.remove_signal_handler(sig)
        await runner.cleanup()
