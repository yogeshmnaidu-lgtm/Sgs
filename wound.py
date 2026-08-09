"""Basic wound and red-region analysis helpers."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class WoundAssessment:
    possible_injury: bool
    red_ratio: float
    bleeding_level: str
    guidance: str

class WoundScanner:
    def assess_rgb_pixels(self, pixels: list[tuple[int, int, int]]) -> WoundAssessment:
        if not pixels:
            return WoundAssessment(False, 0.0, "None", "No image data available.")
        red_like = sum(1 for r, g, b in pixels if r > 120 and r > g * 1.35 and r > b * 1.35)
        ratio = red_like / len(pixels)
        if ratio > 0.18:
            return WoundAssessment(True, ratio, "High", "Apply firm pressure with clean cloth and seek urgent medical help.")
        if ratio > 0.06:
            return WoundAssessment(True, ratio, "Medium", "Clean gently, cover the wound, and monitor bleeding.")
        return WoundAssessment(False, ratio, "Low", "No heavy bleeding detected by the basic scanner.")
