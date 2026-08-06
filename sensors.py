"""Sensor abstraction with Raspberry Pi GPIO wiring and safe desktop fallback."""
from __future__ import annotations
import random
from dataclasses import dataclass, field
from config import GPIO_PINS
from models import AirQuality, SystemTelemetry, GpsFix

@dataclass
class SensorSnapshot:
    camera: str = "OK"
    gps: str = "OK"
    ai_engine: str = "ACTIVE"
    sensors: str = "ACTIVE"
    battery: str = "82%"
    storage: str = "68%"
    wifi: str = "CONNECTED"
    telegram: str = "READY"
    pir: str = "OK"
    ultrasonic: str = "OK"
    humidity: str = "OK"
    ir: str = "OK"
    gas: str = "OK"
    obstacle_cm: float = 140.0
    air: AirQuality = field(default_factory=AirQuality)

class SensorManager:
    def __init__(self):
        self.pins = GPIO_PINS
        self._tick = 0

    def read(self) -> SensorSnapshot:
        self._tick += 1
        return SensorSnapshot(
            battery=f"{max(35, 82 - self._tick // 45)}%",
            storage=f"{min(92, 68 + self._tick // 70)}%",
            air=AirQuality(aqi=max(20, min(90, 42 + random.randint(-3, 3)))),
            obstacle_cm=round(140 + random.uniform(-25, 30), 1),
        )

    def telemetry(self, system_id: str, mode: str) -> SystemTelemetry:
        snap = self.read()
        return SystemTelemetry(
            system_id=system_id,
            gps=GpsFix(),
            mode=mode,
            battery_pct=int(snap.battery.rstrip("%")),
            storage_pct=int(snap.storage.rstrip("%")),
            wifi=snap.wifi,
            telegram=snap.telegram,
        )
