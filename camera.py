"""Camera service with graceful fallback when OpenCV or a camera is unavailable."""
from __future__ import annotations

class CameraService:
    def __init__(self, index: int = 0):
        self.index = index
        self.active = False
        self.cap = None
        try:
            import cv2  # type: ignore
            self.cv2 = cv2
        except Exception:
            self.cv2 = None

    def start(self):
        if self.cv2 and self.cap is None:
            self.cap = self.cv2.VideoCapture(self.index)
        self.active = True

    def stop(self):
        self.active = False
        if self.cap:
            self.cap.release(); self.cap = None

    def read(self):
        if self.active and self.cap:
            ok, frame = self.cap.read()
            if ok:
                return frame
        return None
