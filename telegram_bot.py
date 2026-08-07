"""Telegram emergency alert integration."""
from __future__ import annotations
from pathlib import Path
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramBot:
    def __init__(self, token: str = TELEGRAM_BOT_TOKEN, chat_id: str = TELEGRAM_CHAT_ID):
        self.token = token
        self.chat_id = chat_id

    @property
    def configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def send_message(self, text: str) -> bool:
        if not self.configured:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        import requests
        response = requests.post(url, data={"chat_id": self.chat_id, "text": text}, timeout=12)
        response.raise_for_status()
        return True

    def send_photo(self, image_path: str | Path, caption: str = "SGS evidence") -> bool:
        if not self.configured:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        with Path(image_path).open("rb") as image:
            import requests
            response = requests.post(url, data={"chat_id": self.chat_id, "caption": caption}, files={"photo": image}, timeout=20)
        response.raise_for_status()
        return True
