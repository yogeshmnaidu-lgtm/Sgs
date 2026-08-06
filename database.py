"""SQLite persistence for incidents and activity events."""
from __future__ import annotations
import sqlite3
from datetime import datetime
from config import DB_PATH

class SGSDatabase:
    def __init__(self, path=DB_PATH):
        self.path = path
        self._init()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _init(self):
        with self._connect() as con:
            con.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, ts TEXT, level TEXT, message TEXT)")
            con.execute("CREATE TABLE IF NOT EXISTS evidence (id INTEGER PRIMARY KEY, ts TEXT, kind TEXT, path TEXT, summary TEXT)")

    def add_event(self, message: str, level: str = "INFO"):
        with self._connect() as con:
            con.execute("INSERT INTO events(ts, level, message) VALUES (?, ?, ?)", (datetime.now().isoformat(timespec="seconds"), level, message))
