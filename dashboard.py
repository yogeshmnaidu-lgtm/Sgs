"""Neon SGS Drone Visual dashboard rendered on a responsive Tkinter canvas."""
from __future__ import annotations
import math
import tkinter as tk
from datetime import datetime

from ai import SGSAssistant
from commands import all_commands, response_for
from config import APP_NAME, DEVELOPER, GPS_COORDINATES, LOCATION_NAME, MODE, ORGANIZATION, SYSTEM_ID
from detection import DetectionEngine
from logger import ActivityLog
from maps import MapService
from news import NewsService
from sensors import SensorManager
from weather import WeatherService

BASE_W = 1366
BASE_H = 768
BG = "#020713"
PANEL = "#04111d"
CYAN = "#00d9ff"
BLUE = "#008dff"
GREEN = "#6dff43"
YELLOW = "#ffe94d"
RED = "#ff2d55"
WHITE = "#eaffff"
MUTED = "#8fb7c9"
ORANGE = "#ff9d2e"

class NeonCanvas(tk.Canvas):
    """Canvas with base-resolution scaling helpers."""
    def __init__(self, master):
        super().__init__(master, bg=BG, highlightthickness=0)
        self.scale_factor = 1.0
        self.xoff = 0.0
        self.yoff = 0.0

    def configure_scale(self):
        w = max(self.winfo_width(), 1)
        h = max(self.winfo_height(), 1)
        self.scale_factor = min(w / BASE_W, h / BASE_H)
        self.xoff = (w - BASE_W * self.scale_factor) / 2
        self.yoff = (h - BASE_H * self.scale_factor) / 2

    def sx(self, x: float) -> float:
        return self.xoff + x * self.scale_factor

    def sy(self, y: float) -> float:
        return self.yoff + y * self.scale_factor

    def font(self, size: int, weight: str = "normal"):
        return ("Playfair Display", max(6, int(size * self.scale_factor)), weight)

    def line_scaled(self, *points, **kwargs):
        scaled = []
        for i, value in enumerate(points):
            scaled.append(self.sx(value) if i % 2 == 0 else self.sy(value))
        return self.create_line(*scaled, **kwargs)

    def rect_scaled(self, x1, y1, x2, y2, **kwargs):
        return self.create_rectangle(self.sx(x1), self.sy(y1), self.sx(x2), self.sy(y2), **kwargs)

    def poly_scaled(self, points, **kwargs):
        scaled = []
        for x, y in points:
            scaled.extend([self.sx(x), self.sy(y)])
        return self.create_polygon(*scaled, **kwargs)

    def text_scaled(self, x, y, text, size=10, fill=WHITE, weight="normal", anchor="nw", **kwargs):
        return self.create_text(self.sx(x), self.sy(y), text=text, fill=fill, font=self.font(size, weight), anchor=anchor, **kwargs)

class SGSDashboard(tk.Tk):
    """High-density, image-inspired SGS neon dashboard."""
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.configure(bg=BG)
        self.minsize(1100, 620)
        self.geometry("1366x768")
        self.canvas = NeonCanvas(self)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self._redraw())

        self.sensors = SensorManager()
        self.detector = DetectionEngine()
        self.weather = WeatherService()
        self.news = NewsService()
        self.maps = MapService()
        self.log = ActivityLog()
        self.ai = SGSAssistant()
        self.chat_messages = ["SGS: Guardian dashboard online."]
        self.command_entry = tk.Entry(self, bg="#020914", fg=GREEN, insertbackground=GREEN, relief="flat", font=("Playfair Display", 10))
        self.command_entry.bind("<Return>", self._chat)
        self.command_window = self.canvas.create_window(1044, 733, width=292, height=22, window=self.command_entry, anchor="nw")
        self.after(200, self._tick)

    def _tick(self):
        self.snapshot = self.sensors.read()
        self.weather_report = self.weather.current()
        self.detections = self.detector.detect()
        self.counts = self.detector.counts(self.detections)
        self._redraw()
        self.after(1000, self._tick)

    def _redraw(self):
        if not hasattr(self, "snapshot"):
            return
        c = self.canvas
        c.delete("all")
        c.configure_scale()
        self._draw_background()
        self._draw_header()
        self._draw_camera_scene()
        self._draw_left_stack()
        self._draw_right_stack()
        self._draw_bottom_stack()
        c.itemconfigure(self.command_window, state="normal")
        c.coords(self.command_window, c.sx(1044), c.sy(733))
        c.itemconfigure(self.command_window, width=292 * c.scale_factor, height=22 * c.scale_factor)

    def _draw_background(self):
        c = self.canvas
        c.rect_scaled(0, 0, BASE_W, BASE_H, fill=BG, outline="")
        for x in range(0, BASE_W, 46):
            c.line_scaled(x, 0, x + 160, 90, fill="#072034")
        for y in range(0, BASE_H, 44):
            c.line_scaled(0, y, BASE_W, y + 28, fill="#04182a")

    def _panel(self, x, y, w, h, title, accent=CYAN):
        c = self.canvas
        cut = 10
        points = [(x + cut, y), (x + w - cut, y), (x + w, y + cut), (x + w, y + h - cut), (x + w - cut, y + h), (x + cut, y + h), (x, y + h - cut), (x, y + cut)]
        c.poly_scaled(points, fill=PANEL, outline=accent, width=1.4)
        c.rect_scaled(x + 8, y + 24, x + w - 8, y + h - 8, fill="#020914", outline="#0a2c43")
        c.text_scaled(x + 14, y + 8, title, 10, WHITE, "bold")
        c.line_scaled(x + 10, y + 25, x + w - 10, y + 25, fill="#0b5575")

    def _draw_header(self):
        c = self.canvas
        self._panel(10, 10, 315, 76, "", CYAN)
        c.text_scaled(90, 28, "SGS", 28, WHITE, "bold")
        c.text_scaled(92, 61, "SMART GUARDIAN SYSTEM", 9, WHITE)
        c.poly_scaled([(32, 24), (58, 14), (83, 24), (83, 54), (58, 70), (32, 54)], outline=WHITE, fill="#07111c", width=2)
        c.text_scaled(58, 42, "♜", 22, WHITE, "bold", anchor="center")
        c.text_scaled(683, 15, "SGS DRONE VISUAL", 30, WHITE, "bold", anchor="center")
        c.text_scaled(683, 54, "SMART GUARDIAN SYSTEM 2.0", 13, CYAN, "bold", anchor="center")
        c.poly_scaled([(415, 72), (951, 72), (905, 103), (461, 103)], fill="#04111d", outline=CYAN, width=2)
        c.text_scaled(683, 86, f"LOCATION : {LOCATION_NAME}", 16, CYAN, "bold", anchor="center")
        self._panel(1115, 10, 240, 76, "DRONE CAMERA FOOTAGE", CYAN)
        now = datetime.now()
        c.text_scaled(1140, 39, f"DATE : {now:%d-%m-%Y}\nTIME : {now:%I:%M:%S %p}\nMODE : NIGHT VISION AI", 9, WHITE)
        c.text_scaled(1288, 42, "● REC", 11, RED, "bold")

    def _draw_camera_scene(self):
        c = self.canvas
        x, y, w, h = 205, 105, 920, 545
        c.rect_scaled(x, y, x + w, y + h, fill="#05080c", outline=CYAN, width=2)
        # bright night-road illustration so the camera area is visible even without a real camera
        for i in range(16):
            shade = 10 + i * 4
            c.rect_scaled(x + 2, y + i * h / 16, x + w - 2, y + (i + 1) * h / 16, fill=f"#{shade:02x}{shade+5:02x}{shade+12:02x}", outline="")
        c.create_oval(c.sx(580), c.sy(214), c.sx(640), c.sy(274), fill="#fff4b0", outline="#ffffff")
        for r in range(45, 190, 24):
            c.create_oval(c.sx(610-r), c.sy(244-r), c.sx(610+r), c.sy(244+r), outline="#fff4b0", width=1)
        # trees/buildings
        for bx in [220, 260, 300, 1010, 1060]:
            c.rect_scaled(bx, 145, bx + 34, 650, fill="#061018", outline="#102b36")
            for wy in range(165, 610, 42):
                c.rect_scaled(bx + 7, wy, bx + 26, wy + 14, fill="#ffd45a", outline="")
        for tx in [335, 380, 880, 930, 980]:
            c.line_scaled(tx, 255, tx - 38, 650, fill="#2b170f", width=7)
            for k in range(5):
                c.create_oval(c.sx(tx-85+k*18), c.sy(125+k*12), c.sx(tx+75+k*12), c.sy(310+k*6), fill="#082616", outline="#103d24")
        # road and lane lights
        c.poly_scaled([(385, 650), (545, 340), (780, 340), (1040, 650)], fill="#111821", outline="#23394d")
        c.line_scaled(657, 348, 681, 650, fill=YELLOW, width=2)
        c.line_scaled(704, 350, 760, 650, fill=YELLOW, width=2)
        for ly in range(380, 640, 52):
            c.line_scaled(682, ly, 698, ly + 24, fill="#f7e36b", width=3)
        # vehicles and humans silhouettes
        for vx, vy, color in [(455, 520, BLUE), (690, 455, BLUE), (820, 515, BLUE), (935, 420, BLUE)]:
            c.rect_scaled(vx, vy, vx+95, vy+55, fill="#111722", outline=color, width=2)
            c.create_oval(c.sx(vx+13), c.sy(vy+44), c.sx(vx+28), c.sy(vy+59), fill="#050505", outline="")
            c.create_oval(c.sx(vx+67), c.sy(vy+44), c.sx(vx+82), c.sy(vy+59), fill="#050505", outline="")
            c.rect_scaled(vx+8, vy+8, vx+87, vy+26, fill="#172d3f", outline="")
        for hx, hy in [(350, 465), (580, 390), (995, 492)]:
            c.create_oval(c.sx(hx), c.sy(hy), c.sx(hx+18), c.sy(hy+18), fill=GREEN, outline="")
            c.line_scaled(hx+9, hy+18, hx+9, hy+68, fill=GREEN, width=3)
            c.line_scaled(hx-8, hy+34, hx+26, hy+34, fill=GREEN, width=2)
            c.line_scaled(hx+9, hy+68, hx-6, hy+100, fill=GREEN, width=2)
            c.line_scaled(hx+9, hy+68, hx+25, hy+100, fill=GREEN, width=2)
        for d in self.detections:
            bx = x + d.x * w
            by = y + d.y * h
            bw = d.w * w
            bh = d.h * h
            c.rect_scaled(bx, by, bx + bw, by + bh, outline=d.color, width=1.6)
            c.text_scaled(bx, by - 14, d.label, 9, d.color, "bold")
            info_w = 178 if d.label == "VEHICLE" else 138
            info_h = 22 + 12 * len(d.details)
            ix = min(bx + bw + 9, x + w - info_w - 6)
            iy = max(y + 8, by - 3)
            c.rect_scaled(ix, iy, ix + info_w, iy + info_h, fill="#031018", outline=d.color, width=1.3)
            c.text_scaled(ix + 7, iy + 6, "\n".join(d.details), 7, WHITE)

    def _draw_left_stack(self):
        s = self.snapshot
        w = self.weather_report
        self._panel(10, 100, 185, 182, "SYSTEM STATUS")
        self._kv(26, 137, [("CAMERA", "OK"), ("GPS", "OK"), ("AI ENGINE", "ACTIVE"), ("SENSORS", "ACTIVE"), ("BATTERY", s.battery), ("STORAGE", s.storage), ("WIFI", s.wifi), ("TELEGRAM", s.telegram)])
        self._panel(10, 292, 185, 160, "SENSOR STATUS")
        self._kv(26, 327, [("PIR MOTION", s.pir), ("IR SENSOR", s.ir), ("MQ135 GAS", s.gas), ("DHT22 TEMP", s.humidity), ("ULTRASONIC", s.ultrasonic), ("MICROPHONE", "OK"), ("SPEAKER", "OK")])
        self._panel(10, 462, 185, 123, "WEATHER")
        self.canvas.text_scaled(30, 503, "☁", 28, WHITE)
        self.canvas.text_scaled(102, 500, f"{w.temperature_c}°C", 20, WHITE, "bold")
        self.canvas.text_scaled(104, 528, w.condition.upper(), 8, WHITE)
        self.canvas.text_scaled(26, 548, f"HUMIDITY : {w.humidity_pct}%\nWIND     : {w.wind_kmh} km/h\nVISIBILITY : {w.visibility_km} km", 8, WHITE)
        self._panel(10, 595, 185, 143, "NEWS HEADLINES")
        self.canvas.text_scaled(25, 630, "\n".join(f"• {h}" for h in self.news.headlines()), 8, WHITE)

    def _draw_right_stack(self):
        s = self.snapshot
        self._panel(1140, 100, 215, 113, "OBJECTS DETECTED")
        self.canvas.text_scaled(1164, 134, f"♟  HUMANS     : {self.counts['humans']}\n🚙  VEHICLES   : {self.counts['vehicles']}\n⬡  OBJECTS    : {self.counts['objects']}", 12, WHITE)
        self._panel(1140, 224, 215, 132, "AI ANALYTICS")
        self.canvas.text_scaled(1160, 257, "☑ NO ABNORMAL ACTIVITY\n☑ TRAFFIC FLOW : NORMAL\n☑ PEDESTRIANS : SAFE\n☑ ENVIRONMENT : SAFE\n☑ NO ACCIDENT RISK\n☑ AREA STATUS : SECURE", 8, GREEN)
        self._panel(1140, 367, 215, 134, "AIR QUALITY INDEX")
        self.canvas.text_scaled(1162, 414, str(s.air.aqi), 32, GREEN, "bold")
        self.canvas.text_scaled(1168, 456, s.air.label.upper(), 9, GREEN, "bold")
        self.canvas.text_scaled(1235, 406, f"PM2.5 : {s.air.pm25}\nPM10  : {s.air.pm10}\nCO    : 0.4 ppm\nNO2   : 12 ppb\nO3    : 35 ppb", 8, WHITE)
        self._panel(1140, 512, 215, 152, "SYSTEM TELEMETRY")
        self.canvas.text_scaled(1157, 548, f"DRONE ID : {SYSTEM_ID}\nALTITUDE : 18.6 m\nSPEED    : 12.4 m/s\nGPS      : {GPS_COORDINATES}\nMODE     : {MODE}\nBATTERY  : {s.battery}\nSIGNAL   : STRONG\nRECORDING: ● ON", 8, WHITE)

    def _draw_bottom_stack(self):
        self._panel(10, 650, 310, 108, "COMMAND CENTER")
        self.canvas.text_scaled(26, 684, "> SYSTEM ACTIVE AND MONITORING...\n> ALL SYSTEMS NORMAL\n> NO EMERGENCIES DETECTED\n> DATA LOGGING IN PROGRESS\n> STAY SAFE, STAY SECURE", 8, GREEN)
        self._panel(330, 650, 205, 108, "LIVE MAP")
        self._draw_map(345, 680, 175, 64)
        self._panel(545, 650, 250, 108, "RECENT ACTIVITY LOG")
        self.canvas.text_scaled(560, 684, "\n".join(self.log.items[-6:]), 8, WHITE)
        self._panel(805, 650, 165, 108, "MISSION OBJECTIVE")
        self.canvas.text_scaled(823, 686, "◎ Monitor Environment\n• Detect Anomalies\n• Prevent Accidents\n• Protect Human Lives\n• Real-time Surveillance", 8, WHITE)
        self._panel(980, 650, 376, 108, "DEVELOPER INFO", YELLOW)
        self.canvas.text_scaled(998, 684, f"SMART GUARDIAN SYSTEM (SGS)\nDeveloped & Designed By\n{DEVELOPER}\nBuilding For A Safer Tomorrow", 10, WHITE)
        self.canvas.text_scaled(1295, 703, "🤖", 42, CYAN, "bold", anchor="center")
        self.canvas.text_scaled(1044, 714, "CHAT / COMMAND INPUT", 8, GREEN, "bold")
        self.command_window = self.canvas.create_window(self.canvas.sx(1044), self.canvas.sy(733), width=292 * self.canvas.scale_factor, height=22 * self.canvas.scale_factor, window=self.command_entry, anchor="nw")

    def _draw_map(self, x, y, w, h):
        for road in self.maps.grid_roads(w, h):
            x1, y1, x2, y2 = road
            self.canvas.line_scaled(x + x1, y + y1, x + x2, y + y2, fill="#284354", width=2)
        self.canvas.create_oval(self.canvas.sx(x + w/2 - 8), self.canvas.sy(y + h/2 - 8), self.canvas.sx(x + w/2 + 8), self.canvas.sy(y + h/2 + 8), fill=CYAN, outline=WHITE)
        self.canvas.text_scaled(x + w/2, y + h - 2, LOCATION_NAME, 7, WHITE, anchor="s")

    def _kv(self, x, y, rows):
        for index, (key, value) in enumerate(rows):
            yy = y + index * 18
            self.canvas.text_scaled(x, yy, "●", 10, GREEN)
            self.canvas.text_scaled(x + 18, yy, key, 8, WHITE)
            self.canvas.text_scaled(x + 126, yy, value, 8, GREEN, anchor="nw")

    def _chat(self, _event=None):
        message = self.command_entry.get().strip()
        self.command_entry.delete(0, "end")
        if not message:
            return
        reply = response_for(message) or self.ai.reply(message)
        self.log.add(f"Command processed: {message}")
        self.chat_messages.append(f"You: {message}")
        self.chat_messages.append(f"SGS: {reply}")
        self._redraw()

def run():
    SGSDashboard().mainloop()
