# Smart Guardian System (SGS) 2.0

SGS Visual is a responsive futuristic dashboard for Raspberry Pi safety monitoring. It combines camera overlays, GPIO sensor status, air quality, weather/news placeholders, command center, live-map panel, activity log, chat assistant, and developer branding for **M. Yogesh Naidu / NY Technologies**.

## Run

```bash
python main.py
```

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

## Secrets

Put API keys in `config.py` locally. The repository intentionally leaves NVIDIA, Telegram, Maps, Weather, and News keys blank so real credentials are not committed.

## Project vision

Smart Guardian System watches when humans cannot, speaks when victims cannot, alerts when help is needed, and protects health, hygiene, safety, and life through real-time sensing, computer vision, AI assistance, and automated emergency communication.
