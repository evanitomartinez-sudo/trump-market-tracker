import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, DISCORD_WEBHOOK

def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": False,
    }, timeout=20)
    r.raise_for_status()

def send_discord(text):
    if not DISCORD_WEBHOOK:
        return
    r = requests.post(DISCORD_WEBHOOK, json={"content": text}, timeout=20)
    r.raise_for_status()

def broadcast(text):
    errors = []
    for fn in (send_telegram, send_discord):
        try:
            fn(text)
        except Exception as exc:
            errors.append(str(exc))
    return errors
