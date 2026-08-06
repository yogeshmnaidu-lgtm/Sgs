"""NVIDIA-compatible AI assistant wrapper with offline safety responses."""
from __future__ import annotations
from config import NVIDIA_API_KEY

class SGSAssistant:
    def reply(self, text: str) -> str:
        t = text.lower().strip()
        if any(w in t for w in ["gas", "smoke", "fire"]):
            return "Emergency guidance: move to fresh air, avoid sparks, evacuate, and contact emergency services immediately."
        if any(w in t for w in ["wound", "bleeding", "injury"]):
            return "First aid: apply firm pressure with a clean cloth, keep the person calm, and seek medical help if bleeding is heavy."
        if any(w in t for w in ["scared", "anxious", "panic"]):
            return "I am here with you. Breathe in for four seconds, hold, breathe out slowly, and contact a trusted person if you feel unsafe."
        if NVIDIA_API_KEY:
            return "NVIDIA AI key is configured. Connect your preferred NVIDIA endpoint in ai.py for live model responses."
        return "SGS is monitoring camera, sensors, weather, map, alerts, and emergency commands. How can I help?"
