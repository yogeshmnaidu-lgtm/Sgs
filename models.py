"""Shared SGS data models."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GpsFix:
    latitude: float = 13.0313
    longitude: float = 77.6351
    label: str = "Kalyan Nagar (HRBR Layout)"

@dataclass
class WeatherReport:
    condition: str = "Partly Cloudy"
    icon: str = "☁"
    temperature_c: float = 29.0
    humidity_pct: float = 62.0
    wind_kmh: float = 8.0
    visibility_km: float = 10.0

@dataclass
class AirQuality:
    aqi: int = 42
    label: str = "Good"
    smoke: str = "Low"
    lpg: str = "None"
    co2: str = "Normal"
    pm25: str = "18 µg/m³"
    pm10: str = "32 µg/m³"

@dataclass
class SystemTelemetry:
    system_id: str
    gps: GpsFix
    mode: str
    battery_pct: int = 82
    storage_pct: int = 68
    wifi: str = "CONNECTED"
    telegram: str = "READY"
    recording: bool = True
    updated_at: datetime = field(default_factory=datetime.now)
