"""Configuration for Smart Guardian System (SGS)."""
from pathlib import Path

APP_NAME = "SGS Visual"
SYSTEM_ID = "SGS-DRN-001"
DEVELOPER = "M. Yogesh Naidu & Krishna Dev"
ORGANIZATION = "NY Technologies"
MODE = "Night Vision AI Mode"
LOCATION_NAME = "KVDRDO BLR"
GPS_COORDINATES = "12.9916° N, 77.6680° E"

# Fill these locally. Do not commit real secrets.
NVIDIA_API_KEY = ""
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
MAPS_API_KEY = ""
WEATHER_API_KEY = ""
NEWS_API_KEY = ""

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
MODEL_DIR = BASE_DIR / "models"
EVIDENCE_DIR = BASE_DIR / "evidence"
DB_PATH = BASE_DIR / "sgs.sqlite3"
LOG_PATH = BASE_DIR / "sgs.log"

GPIO_PINS = {
    "gas_analog": 19,
    "gas_digital": 13,
    "pir_data": 18,
    "humidity_data": 26,
    "ultrasonic_trig": 5,
    "ultrasonic_echo": 6,
    "ir_data": 17,
    "mpr121_scl": 23,
    "mpr121_sda": 24,
    "color_sensor_out": 15,
    "touch_sensor_sig": 14,
}

COMMANDS = [
    "Hello SGS", "Scan wound", "Check pulse", "Start camera", "Stop camera",
    "Enable monitoring", "Disable alarms", "Emergency mode", "Gas leak",
    "Call ambulance", "Call police", "Fire emergency", "Medical emergency",
    "Heart attack", "Stroke", "Choking", "Breathing problem", "Poison",
    "Allergic reaction", "Earthquake", "Tsunami", "Chemical spill",
    "Bomb threat", "Radiation leak", "Kidnapping", "Robbery", "Assault",
    "Weather", "News", "Help", "Shutdown", "Restart", "Diagnostics",
    "Sensor status", "Admin mode", "Touch scan", "Color scan", "Vitals",
]
