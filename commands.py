"""Command registry and emergency guidance snippets."""
from __future__ import annotations
from config import COMMANDS

EMERGENCY_RESPONSES = {
    "gas leak": "Evacuate immediately, avoid switches or flames, open ventilation if safe, and call emergency services.",
    "fire emergency": "Move away from smoke, crawl low, use an extinguisher only if trained, and call fire services.",
    "scan wound": "Scanning for red-region injury cues. Apply clean pressure if bleeding is visible.",
    "check pulse": "Place palm near the camera area and remain still while pulse estimation runs.",
    "medical emergency": "Keep the patient still, check breathing, and contact medical responders immediately.",
}

def all_commands() -> list[str]:
    return list(COMMANDS)

def response_for(command: str) -> str | None:
    key = command.lower().strip()
    return EMERGENCY_RESPONSES.get(key)
