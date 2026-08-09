"""Text-to-speech and voice output utilities with safe fallback."""
from __future__ import annotations
import shutil
import subprocess

class VoiceAssistant:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.last_spoken = ""

    def speak(self, text: str) -> bool:
        self.last_spoken = text
        if not self.enabled:
            return False
        command = shutil.which("espeak") or shutil.which("spd-say")
        if not command:
            return False
        subprocess.Popen([command, text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
