# main.py
from flask import Flask, request
from datetime import datetime
import requests
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# Trust the first proxy in front of us so request.remote_addr is real client IP
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1368661794326974555/1s8zTlN5aPPn3RjbL-faGmWWOnnbD4SqQ5Fd8VF6PaU4OmmiJCucrXHW8LFNAQMrSvee"

@app.route('/')
def log_ip():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')

    # Geo‑lookup
    try:
        geo = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,city,regionName,country",
            timeout=3
        ).json()
        if geo.get("status") == "success":
            location = f"{geo['city']}, {geo['regionName']}, {geo['country']}"
        else:
            location = "Unknown, , "
    except Exception:
        location = "Unknown, , "

    message = (
        f"New click!\n"
        f"IP: {ip}\n"
        f"Location: {location}\n"
        f"UA: {ua}"
    )

    # Post to Discord (Discord expects 'content', not 'text')
    try:
        requests.post(
            WEBHOOK_URL,
            json={"content": message},
            timeout=5
        )
    except Exception as e:
        with open("webhook_errors.log", "a") as err:
            err.write(f"{datetime.now()} — webhook error: {e}\n")

    with open("ip_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {ip} - {location} - {ua}\n")

    return "Testing Testing Motherfucker"

if __name__ == '__main__':
    app.run()
