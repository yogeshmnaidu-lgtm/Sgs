"""Camera service with graceful fallback when OpenCV or a camera is unavailable."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from config import EVIDENCE_DIR

class CameraService:
    def __init__(self, index: int = 0):
        self.index = index
        self.active = False
        self.cap = None
        try:
            import cv2  # type: ignore
            self.cv2 = cv2
        except ImportError:
            self.cv2 = None

    def start(self):
        if self.cv2 and self.cap is None:
            self.cap = self.cv2.VideoCapture(self.index)
        self.active = True

    def stop(self):
        self.active = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def read(self):
        if self.active and self.cap:
            ok, frame = self.cap.read()
            if ok:
                return frame
        return None

    def capture_evidence(self, prefix: str = "evidence") -> Path | None:
        frame = self.read()
        if frame is None or not self.cv2:
            return None
        EVIDENCE_DIR.mkdir(exist_ok=True)
        path = EVIDENCE_DIR / f"{prefix}_{datetime.now():%Y%m%d_%H%M%S}.jpg"
        self.cv2.imwrite(str(path), frame)
        return path
