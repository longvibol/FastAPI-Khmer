import requests
from app.config import settings


def send_telegram_alert(message: str) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False
