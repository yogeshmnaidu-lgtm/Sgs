"""Contactless pulse estimation support functions."""
from __future__ import annotations
from dataclasses import dataclass
from statistics import mean

@dataclass
class PulseReading:
    bpm: int
    status: str
    confidence: float

class PulseEstimator:
    def estimate_from_green_signal(self, samples: list[float], fps: float = 30.0) -> PulseReading:
        if len(samples) < 30 or fps <= 0:
            return PulseReading(0, "Insufficient data", 0.0)
        avg = mean(samples)
        crossings = 0
        was_above = samples[0] > avg
        for value in samples[1:]:
            above = value > avg
            if above != was_above:
                crossings += 1
            was_above = above
        beats = max(1, crossings // 2)
        seconds = len(samples) / fps
        bpm = int(beats * 60 / seconds)
        status = "Normal" if 55 <= bpm <= 105 else "Review"
        confidence = min(0.95, max(0.2, len(samples) / 300))
        return PulseReading(bpm, status, confidence)
