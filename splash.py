"""Startup splash text for SGS."""
from __future__ import annotations

SPLASH_LINES = [
    "SMART GUARDIAN SYSTEM 2.0",
    "AI emergency monitoring online",
    "Camera • Sensors • Voice • Telegram • Evidence",
]

def text() -> str:
    return "\n".join(SPLASH_LINES)
