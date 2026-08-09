"""Camera service for AirDroid/IP webcam streams, USB fallback, and evidence capture."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import importlib.util
from config import CAMERA_STREAM_URL, CAMERA_SOURCE, EVIDENCE_DIR

class CameraService:
    """OpenCV camera wrapper that prefers the configured AirDroid stream URL."""

    def __init__(self, source: str | int | None = None):
        self.source = CAMERA_STREAM_URL if source is None else source
        self.usb_source = CAMERA_SOURCE
        self.active = False
        self.cap = None
        self.last_error = ""

    @property
    def cv2_available(self) -> bool:
        return importlib.util.find_spec("cv2") is not None

    def _cv2(self):
        import cv2  # type: ignore
        return cv2

    def start(self) -> bool:
        if not self.cv2_available:
            self.last_error = "OpenCV is not installed"
            self.active = False
            return False
        cv2 = self._cv2()
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened() and self.source != self.usb_source:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.usb_source)
        self.active = bool(self.cap and self.cap.isOpened())
        self.last_error = "" if self.active else f"Unable to open camera source: {self.source}"
        return self.active

    def stop(self):
        self.active = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def read(self):
        if not self.active or not self.cap:
            return None
        ok, frame = self.cap.read()
        if ok:
            return frame
        self.last_error = "Camera frame unavailable"
        return None

    def capture_evidence(self, prefix: str = "evidence") -> Path | None:
        frame = self.read()
        if frame is None or not self.cv2_available:
            return None
        cv2 = self._cv2()
        EVIDENCE_DIR.mkdir(exist_ok=True)
        path = EVIDENCE_DIR / f"{prefix}_{datetime.now():%Y%m%d_%H%M%S}.jpg"
        cv2.imwrite(str(path), frame)
        return path
