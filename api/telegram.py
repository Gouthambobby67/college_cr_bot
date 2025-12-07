import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telegram import Update
from bot import build_application

application = None
try:
    application = build_application()
except Exception:
    application = None

app = FastAPI()

@app.post("/")
async def telegram_webhook(request: Request):
    if application is None:
        return JSONResponse({"error": "application not initialized"}, status_code=500)
    secret_env = os.getenv("TELEGRAM_SECRET_TOKEN")
    if secret_env:
        header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if header != secret_env:
            return JSONResponse({"error": "invalid secret token"}, status_code=401)
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return JSONResponse({"ok": True})

@app.get("/setup")
async def setup_webhook(secret: str | None = None):
    if application is None:
        return JSONResponse({"error": "application not initialized"}, status_code=500)
    url = os.getenv("WEBHOOK_URL")
    if not url:
        return JSONResponse({"error": "WEBHOOK_URL not set"}, status_code=400)
    admin_secret = os.getenv("ADMIN_SECRET")
    if admin_secret and secret != admin_secret:
        return JSONResponse({"error": "forbidden"}, status_code=403)
    secret_token = os.getenv("TELEGRAM_SECRET_TOKEN")
    if secret_token:
        await application.bot.set_webhook(url, secret_token=secret_token)
    else:
        await application.bot.set_webhook(url)
    return JSONResponse({"ok": True, "url": url, "secret_token_set": bool(secret_token)})
