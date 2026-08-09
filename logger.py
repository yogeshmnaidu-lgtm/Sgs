"""Application logging helpers."""
from __future__ import annotations
import logging
from datetime import datetime
from config import LOG_PATH
from database import SGSDatabase

logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class ActivityLog:
    def __init__(self, max_items: int = 80):
        self.max_items = max_items
        self.items: list[str] = []
        self.db = SGSDatabase()
        self.add("SGS dashboard initialized")
        self.add("Camera online")
        self.add("AI engine started")
        self.add("All sensors normal")

    def add(self, message: str, level: str = "INFO") -> str:
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.items.append(entry)
        self.items = self.items[-self.max_items:]
        logging.log(getattr(logging, level, logging.INFO), message)
        self.db.add_event(message, level)
        return entry
