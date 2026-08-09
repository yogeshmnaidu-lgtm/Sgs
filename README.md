# Smart Guardian System (SGS) 2.0

SGS Visual is a Raspberry Pi-ready emergency response dashboard for **Smart Guardian System**. It is designed around a futuristic robotic UI with a live camera visual, AI detection overlays, sensor status, weather, news, live-map panel, command center, activity log, chat assistant, air-quality index, colour sensor readings, touch-triggered vitals, startup voice announcement, and developer branding for **M. Yogesh Naidu / NY Technologies**.

## Run

```bash
python main.py
```

The app uses safe desktop fallbacks, so it can open without Raspberry Pi GPIO hardware, OpenCV camera access, Telegram credentials, or cloud API keys.

## Main files

| File | Purpose |
| --- | --- |
| `main.py` | Application entry point |
| `dashboard.py` | Responsive Tkinter SGS Visual UI |
| `config.py` | IDs, location, GPIO pins, commands, blank API key placeholders |
| `sensors.py` | Raspberry Pi sensor abstraction and offline sensor snapshots |
| `detection.py` | AI detection overlay data for humans, vehicles, objects, and blood risk |
| `camera.py` | Optional OpenCV camera service and evidence capture |
| `ai.py` | Offline emergency assistant plus NVIDIA endpoint hook |
| `telegram_bot.py` | Telegram message/photo sender when credentials are configured |
| `voice.py` | Text-to-speech helper using `espeak` or `spd-say` when available |
| `wound.py` | Basic red-region wound/bleeding assessment helper |
| `pulse.py` | Contactless pulse signal estimator helper |
| `database.py` / `logger.py` | SQLite event/evidence tables and activity logging |
| `weather.py`, `news.py`, `maps.py` | Offline providers ready to be replaced with live APIs |


## AirDroid phone camera feed

SGS now defaults to the AirDroid/IP webcam stream at:

```text
http://192.168.0.100:4747/video
```

If OpenCV can read that stream directly, the dashboard shows it inside the central camera visual. If your system needs a Linux webcam bridge, run this before starting SGS:

```bash
sudo ffmpeg -i http://192.168.0.100:4747/video -f v4l2 -pix_fmt yuv420p /dev/video0
```

The app still falls back to `/dev/video0`/camera index `0` if the AirDroid stream cannot be opened, and it displays the neon simulation if no frame is available.

## Hardware wiring

| Module | Pin |
| --- | --- |
| MQ gas AO | GPIO 19 |
| MQ gas DO | GPIO 13 |
| PIR data | GPIO 18 |
| DHT data | GPIO 26 |
| Ultrasonic trig | GPIO 5 |
| Ultrasonic echo | GPIO 6 |
| IR data | GPIO 17 |
| MPR121 SCL | GPIO 23 |
| MPR121 SDA | GPIO 24 |
| Colour sensor OUT | GPIO 15 |
| Touch sensor SIG | GPIO 14 |

## API keys and secrets

Real keys must be added locally in `config.py` or loaded from your own environment. The repository intentionally keeps these values blank:

- `NVIDIA_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `MAPS_API_KEY`
- `WEATHER_API_KEY`
- `NEWS_API_KEY`

Never commit real API keys to GitHub.

## Project vision

Smart Guardian System watches when humans cannot, speaks when victims cannot, alerts when help is needed, and protects health, hygiene, safety, and life through real-time sensing, computer vision, AI assistance, voice guidance, evidence capture, and automated emergency communication.
