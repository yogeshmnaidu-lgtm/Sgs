"""News provider for dashboard headline rotation."""
from __future__ import annotations

class NewsService:
    def headlines(self) -> list[str]:
        return [
            "City traffic normal",
            "No major incidents reported",
            "Good air quality in your area",
            "Police patrolling increased",
            "Stay safe, stay alert",
        ]
