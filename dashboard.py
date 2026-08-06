"""Responsive futuristic Tkinter dashboard for Smart Guardian System."""
from __future__ import annotations
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

BG = "#030812"
PANEL = "#071522"
PANEL_DARK = "#02070c"
CYAN = "#00d9ff"
GREEN = "#78ff42"
YELLOW = "#ffe84a"
RED = "#ff3158"
TEXT = "#e9fbff"
MUTED = "#8fb8c7"

class SGSDashboard(tk.Tk):
    """Main adaptive UI for SGS safety monitoring."""

    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.configure(bg=BG)
        self.minsize(1180, 720)
        self.geometry("1366x768")

        self.sensors = SensorManager()
        self.detector = DetectionEngine()
        self.weather = WeatherService()
        self.news = NewsService()
        self.maps = MapService()
        self.log = ActivityLog()
        self.ai = SGSAssistant()
        self.detections = []

        self.font_title = ("Playfair Display", 28, "bold")
        self.font_head = ("Playfair Display", 12, "bold")
        self.font_body = ("Playfair Display", 9)
        self.font_small = ("Playfair Display", 8)
        self._build_layout()
        self.after(250, self._tick)

    def _panel(self, parent, title: str):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=CYAN, highlightthickness=1)
        tk.Label(frame, text=title, bg=PANEL, fg=TEXT, font=self.font_head, anchor="w").pack(fill="x", padx=8, pady=(5, 1))
        return frame

    def _text_panel(self, parent, title: str, height: int):
        frame = self._panel(parent, title)
        text = tk.Text(frame, height=height, bg=PANEL_DARK, fg=TEXT, insertbackground=TEXT, font=self.font_body, bd=0, wrap="word")
        text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        return frame, text

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_header()
        self._build_left_column()
        self._build_center()
        self._build_right_column()
        self._build_bottom_bar()

    def _build_header(self):
        header = tk.Frame(self, bg=BG)
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=6)
        header.grid_columnconfigure(1, weight=1)
        tk.Label(header, text="SGS", fg=TEXT, bg=BG, font=("Playfair Display", 25, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(header, text="SMART GUARDIAN SYSTEM", fg=MUTED, bg=BG, font=self.font_body).grid(row=1, column=0, sticky="w")
        tk.Label(header, text="SGS VISUAL", fg=TEXT, bg=BG, font=self.font_title).grid(row=0, column=1, sticky="n")
        tk.Label(header, text=f"LOCATION : {LOCATION_NAME}", fg=CYAN, bg=BG, font=("Playfair Display", 15, "bold")).grid(row=1, column=1, sticky="n")
        self.time_lbl = tk.Label(header, text="", fg=TEXT, bg=BG, font=self.font_body, justify="left")
        self.time_lbl.grid(row=0, column=2, rowspan=2, sticky="e")

    def _build_left_column(self):
        left = tk.Frame(self, bg=BG, width=220)
        left.grid(row=1, column=0, sticky="nsew", padx=(8, 4))
        self.status_frame, self.status_box = self._text_panel(left, "SYSTEM STATUS", 10)
        self.status_frame.pack(fill="x", pady=4)
        self.sensor_frame, self.sensor_box = self._text_panel(left, "SENSOR STATUS", 8)
        self.sensor_frame.pack(fill="x", pady=4)
        self.weather_frame, self.weather_box = self._text_panel(left, "WEATHER", 5)
        self.weather_frame.pack(fill="x", pady=4)
        self.news_frame, self.news_box = self._text_panel(left, "NEWS HEADLINES", 6)
        self.news_frame.pack(fill="both", expand=True, pady=4)

    def _build_center(self):
        center = tk.Frame(self, bg=BG)
        center.grid(row=1, column=1, sticky="nsew")
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(0, weight=1)
        self.camera = tk.Canvas(center, bg="#05080d", highlightbackground=CYAN, highlightthickness=1)
        self.camera.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

    def _build_right_column(self):
        right = tk.Frame(self, bg=BG, width=240)
        right.grid(row=1, column=2, sticky="nsew", padx=(4, 8))
        self.objects_frame, self.objects_box = self._text_panel(right, "OBJECTS DETECTED", 4)
        self.objects_frame.pack(fill="x", pady=4)
        self.analytics_frame, self.analytics_box = self._text_panel(right, "AI ANALYTICS", 7)
        self.analytics_frame.pack(fill="x", pady=4)
        self.commands_frame, self.commands_box = self._text_panel(right, "COMMANDS LIST", 8)
        self.commands_frame.pack(fill="both", expand=True, pady=4)
        self.aqi_frame, self.aqi_box = self._text_panel(right, "AIR QUALITY INDEX", 7)
        self.aqi_frame.pack(fill="x", pady=4)
        self.dev_frame, self.dev_box = self._text_panel(right, "DEVELOPER INFO", 5)
        self.dev_frame.pack(fill="x", pady=4)

    def _build_bottom_bar(self):
        bottom = tk.Frame(self, bg=BG)
        bottom.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 8))
        for col in range(5):
            bottom.grid_columnconfigure(col, weight=1, uniform="bottom")
        self.command_frame, self.command_box = self._text_panel(bottom, "COMMAND CENTER", 5)
        self.command_frame.grid(row=0, column=0, sticky="nsew", padx=4)
        self.info_frame, self.info_box = self._text_panel(bottom, "SYSTEM INFO", 5)
        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=4)
        self.map_frame = self._panel(bottom, "LIVE MAP")
        self.map_frame.grid(row=0, column=2, sticky="nsew", padx=4)
        self.map_canvas = tk.Canvas(self.map_frame, height=132, bg="#07101b", highlightthickness=0)
        self.map_canvas.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.activity_frame, self.activity_box = self._text_panel(bottom, "RECENT ACTIVITY LOG", 6)
        self.activity_frame.grid(row=0, column=3, sticky="nsew", padx=4)
        self.chat_frame = self._panel(bottom, "CHAT SYSTEM")
        self.chat_frame.grid(row=0, column=4, sticky="nsew", padx=4)
        self.chat_log = tk.Text(self.chat_frame, height=4, bg=PANEL_DARK, fg=TEXT, insertbackground=TEXT, font=self.font_body, bd=0)
        self.chat_log.pack(fill="both", expand=True, padx=8)
        self.chat_entry = tk.Entry(self.chat_frame, bg="#07101b", fg=TEXT, insertbackground=TEXT, bd=0)
        self.chat_entry.pack(fill="x", padx=8, pady=6)
        self.chat_entry.bind("<Return>", self._chat)

    def _write(self, widget: tk.Text, content: str):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", content)
        widget.config(state="disabled")

    def _tick(self):
        snapshot = self.sensors.read()
        weather = self.weather.current()
        self.detections = self.detector.detect()
        counts = self.detector.counts(self.detections)
        now = datetime.now()

        self.time_lbl.config(text=f"DRONE CAMERA FOOTAGE  ● REC\nDATE : {now:%d-%m-%Y}\nTIME : {now:%I:%M:%S %p}\nMODE : {MODE}")
        self._write(self.status_box, "\n".join([
            f"● Camera        {snapshot.camera}", f"● GPS           {snapshot.gps}", f"● AI Engine     {snapshot.ai_engine}",
            f"● Sensors       {snapshot.sensors}", f"● Battery       {snapshot.battery}", f"● Storage       {snapshot.storage}",
            f"● WiFi          {snapshot.wifi}", f"● Telegram      {snapshot.telegram}",
        ]))
        self._write(self.sensor_box, "\n".join([
            f"PIR Motion      {snapshot.pir}", f"IR Sensor       {snapshot.ir}", f"MQ Gas          {snapshot.gas}",
            f"DHT Humidity    {snapshot.humidity}", f"Ultrasonic     {snapshot.ultrasonic}", "Microphone      OK", "Speaker         OK",
        ]))
        self._write(self.weather_box, f"{weather.icon}  {weather.temperature_c}°C  {weather.condition}\nHumidity : {weather.humidity_pct}%\nWind : {weather.wind_kmh} km/h\nVisibility : {weather.visibility_km} km")
        self._write(self.news_box, "\n".join(f"• {item}" for item in self.news.headlines()))
        self._write(self.objects_box, f"Humans   : {counts['humans']}\nVehicles : {counts['vehicles']}\nObjects  : {counts['objects']}\nBlood    : Low risk")
        self._write(self.analytics_box, "☑ No abnormal activity\n☑ Traffic flow normal\n☑ Pedestrians safe\n☑ Environment safe\n☑ No accident risk\n☑ Area status secure")
        self._write(self.commands_box, "\n".join(f"• {cmd}" for cmd in all_commands()))
        self._write(self.aqi_box, f"AQI : {snapshot.air.aqi}\nAir Quality : {snapshot.air.label}\nSmoke : {snapshot.air.smoke}\nLPG : {snapshot.air.lpg}\nCO2 : {snapshot.air.co2}\nPM2.5 : {snapshot.air.pm25}\nPM10 : {snapshot.air.pm10}")
        self._write(self.dev_box, f"SMART GUARDIAN SYSTEM (SGS)\nDeveloped & Designed By\n{DEVELOPER}\n{ORGANIZATION}\nBuilding For A Safer Tomorrow")
        self._write(self.command_box, "> SYSTEM ACTIVE AND MONITORING...\n> ALL SYSTEMS NORMAL\n> NO EMERGENCIES DETECTED\n> DATA LOGGING IN PROGRESS\n> STAY SAFE, STAY SECURE")
        self._write(self.info_box, f"System ID : {SYSTEM_ID}\nGPS       : {GPS_COORDINATES}\nMode      : {MODE}\nObstacle  : {snapshot.obstacle_cm} cm")
        self._write(self.activity_box, "\n".join(self.log.items[-6:]))
        self._draw_camera()
        self._draw_map()
        self.after(1000, self._tick)

    def _draw_camera(self):
        w = max(self.camera.winfo_width(), 720)
        h = max(self.camera.winfo_height(), 430)
        self.camera.delete("all")
        for i in range(30):
            self.camera.create_line(0, i * h / 30, w, i * h / 30, fill="#071827")
        self.camera.create_rectangle(8, 8, w - 8, h - 8, outline="#0b5070", width=2)
        self.camera.create_text(w / 2, 28, text="LIVE CAMERA VISUAL - AI DETECTION OVERLAY", fill=CYAN, font=self.font_head)
        horizon = int(h * 0.45)
        self.camera.create_rectangle(10, horizon, w - 10, h - 10, fill="#071018", outline="")
        self.camera.create_polygon(w * .20, h - 10, w * .46, horizon, w * .54, horizon, w * .80, h - 10, fill="#121922", outline="#19364d")
        for x in range(30, int(w), 110):
            self.camera.create_line(x, h - 10, w / 2, horizon, fill="#1b3444")
        for d in self.detections:
            x, y, bw, bh = d.x * w, d.y * h, d.w * w, d.h * h
            self.camera.create_rectangle(x, y, x + bw, y + bh, outline=d.color, width=2)
            self.camera.create_text(x, y - 10, text=d.label, fill=d.color, font=self.font_head, anchor="w")
            info_w = 230
            info_h = 20 + 14 * len(d.details)
            box_x = min(x + bw + 10, w - info_w - 14)
            self.camera.create_rectangle(box_x, y, box_x + info_w, y + info_h, outline=d.color, fill="#031018")
            self.camera.create_text(box_x + 8, y + 8, text="\n".join(d.details), fill=TEXT, font=self.font_small, anchor="nw")

    def _draw_map(self):
        w = max(self.map_canvas.winfo_width(), 190)
        h = max(self.map_canvas.winfo_height(), 115)
        self.map_canvas.delete("all")
        for road in self.maps.grid_roads(w, h):
            self.map_canvas.create_line(*road, fill="#1b3444", width=2)
        self.map_canvas.create_oval(w / 2 - 9, h / 2 - 9, w / 2 + 9, h / 2 + 9, fill=CYAN, outline="white")
        self.map_canvas.create_line(w / 2, h / 2, w / 2, h / 2 + 26, fill=CYAN)
        self.map_canvas.create_text(w / 2, h - 13, text=LOCATION_NAME, fill=TEXT, font=self.font_small)

    def _chat(self, _event=None):
        message = self.chat_entry.get().strip()
        self.chat_entry.delete(0, "end")
        if not message:
            return
        command_reply = response_for(message)
        reply = command_reply or self.ai.reply(message)
        self.chat_log.insert("end", f"You: {message}\nSGS: {reply}\n")
        self.log.add(f"Command processed: {message}")

def run():
    SGSDashboard().mainloop()
