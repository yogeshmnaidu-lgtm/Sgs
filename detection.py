"""Computer-vision detections and overlay rendering."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass
class Detection:
    label: str
    x: float
    y: float
    w: float
    h: float
    color: str
    details: list[str]

class DetectionEngine:
    def detect(self, frame=None) -> list[Detection]:
        return [
            Detection("HUMAN", .18, .50, .08, .24, "#82ff2a", ["Age: 24-32", "Injured: No", "Pulse: Normal", "Body Temp: Normal"]),
            Detection("VEHICLE", .42, .58, .16, .20, "#00b8ff", ["Speed: 32 km/h", "Seatbelts: Normal", "Rash Driving: No", "Speed Status: Normal", "Accident Probability: None", "Registered Name: Unknown"]),
            Detection("OBJECT", .68, .18, .10, .14, "#ffe84a", ["Type: Street Light", "Status: Normal"]),
            Detection("OBJECT", .78, .36, .12, .18, "#83ff3a", ["Type: Tree", "Status: Normal"]),
            Detection("BLOOD", .30, .72, .07, .07, "#ff3158", ["Heavy Bleeding: No", "Cause: Unknown"]),
        ]

    @staticmethod
    def counts(detections: Iterable[Detection]) -> dict[str, int]:
        ds = list(detections)
        return {
            "humans": sum(d.label == "HUMAN" for d in ds),
            "vehicles": sum(d.label == "VEHICLE" for d in ds),
            "objects": sum(d.label == "OBJECT" for d in ds),
        }
