"""Map data helpers for the SGS live-map panel."""
from __future__ import annotations
from models import GpsFix

class MapService:
    def current_fix(self) -> GpsFix:
        return GpsFix()

    def grid_roads(self, width: int, height: int) -> list[tuple[int, int, int, int]]:
        roads = []
        for i in range(7):
            roads.append((int(i * width / 6), 26, int(width - i * width / 8), height))
            roads.append((0, int(34 + i * (height - 42) / 6), width, int(18 + i * (height - 30) / 7)))
        return roads
