"""Sensor abstraction with Raspberry Pi GPIO wiring and safe desktop fallback."""
from __future__ import annotations
import math
import random
from dataclasses import dataclass, field
from config import GPIO_PINS
from models import AirQuality, SystemTelemetry, GpsFix

@dataclass
class PersonVitals:
    name: str = "Unknown"
    heartbeat_bpm: int = 78
    pulse_status: str = "Normal"
    oxygen_pct: int = 98
    skin_temp_c: float = 36.7
    stress_level: str = "Low"
    touch_detected: bool = False

@dataclass
class ColorReading:
    detected_color: str = "Neutral"
    red: int = 82
    green: int = 196
    blue: int = 255
    frequency_hz: int = 1230
    surface_status: str = "Normal"

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
    color_sensor: str = "OK"
    touch_sensor: str = "READY"
    obstacle_cm: float = 140.0
    air: AirQuality = field(default_factory=AirQuality)
    vitals: PersonVitals = field(default_factory=PersonVitals)
    color: ColorReading = field(default_factory=ColorReading)

class SensorManager:
    def __init__(self):
        self.pins = GPIO_PINS
        self._tick = 0

    def read(self) -> SensorSnapshot:
        self._tick += 1
        touch_active = (self._tick // 5) % 2 == 1
        heartbeat = int(78 + math.sin(self._tick / 2.7) * 6 + random.uniform(-2, 2))
        oxygen = max(95, min(100, int(98 + math.sin(self._tick / 3.4) * 1.5)))
        skin_temp = round(36.7 + math.sin(self._tick / 4.0) * 0.4 + random.uniform(-0.1, 0.1), 1)
        colors = [
            ("Cyan", 72, 218, 255, "Normal"),
            ("Green", 92, 255, 94, "Healthy"),
            ("Red Alert", 255, 64, 82, "Possible blood/fire cue"),
            ("Amber", 255, 184, 62, "Caution"),
        ]
        color_name, red, green, blue, surface = colors[(self._tick // 4) % len(colors)]
        vitals = PersonVitals(
            heartbeat_bpm=heartbeat,
            pulse_status="Normal" if 55 <= heartbeat <= 105 else "Review",
            oxygen_pct=oxygen,
            skin_temp_c=skin_temp,
            stress_level="Low" if heartbeat < 88 else "Medium",
            touch_detected=touch_active,
        )
        return SensorSnapshot(
            battery=f"{max(35, 82 - self._tick // 45)}%",
            storage=f"{min(92, 68 + self._tick // 70)}%",
            touch_sensor="TOUCHED" if touch_active else "READY",
            air=AirQuality(aqi=max(20, min(90, 42 + random.randint(-3, 3)))),
            obstacle_cm=round(140 + random.uniform(-25, 30), 1),
            vitals=vitals,
            color=ColorReading(color_name, red, green, blue, int(1180 + math.sin(self._tick / 2) * 130), surface),
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
