"""NVIDIA-compatible AI assistant wrapper with offline safety responses."""
from __future__ import annotations
from commands import response_for
from config import NVIDIA_API_KEY

SYSTEM_PROMPT = (
    "You are SGS, a calm emergency safety assistant. Give short, practical, safe guidance. "
    "For medical, fire, crime, or gas emergencies, recommend contacting local emergency services."
)

class SGSAssistant:
    def __init__(self, api_key: str = NVIDIA_API_KEY, endpoint: str = ""):
        self.api_key = api_key
        self.endpoint = endpoint

    def reply(self, text: str) -> str:
        command = response_for(text)
        if command:
            return command
        t = text.lower().strip()
        if any(w in t for w in ["gas", "smoke", "fire"]):
            return "Move to fresh air, avoid sparks, evacuate if unsafe, and contact emergency services immediately."
        if any(w in t for w in ["wound", "bleeding", "injury"]):
            return "Apply firm pressure with a clean cloth, keep the person calm, and seek medical help if bleeding is heavy."
        if any(w in t for w in ["scared", "anxious", "panic"]):
            return "I am here with you. Breathe in for four seconds, hold briefly, breathe out slowly, and contact someone trusted if you feel unsafe."
        if self.api_key and self.endpoint:
            return self._remote_reply(text)
        return "SGS is monitoring camera, sensors, weather, map, alerts, and emergency commands. How can I help?"

    def _remote_reply(self, text: str) -> str:
        payload = {"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}]}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        import requests
        response = requests.post(self.endpoint, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "SGS AI response received.")
