"""Weather provider with API-ready shape and deterministic offline fallback."""
from __future__ import annotations
import random
from models import WeatherReport

class WeatherService:
    def current(self) -> WeatherReport:
        return WeatherReport(
            temperature_c=round(29 + random.uniform(-0.7, 0.7), 1),
            humidity_pct=round(62 + random.uniform(-3, 3), 1),
            wind_kmh=round(8 + random.uniform(-1.5, 1.5), 1),
            visibility_km=round(10 + random.uniform(-0.8, 0.8), 1),
        )
