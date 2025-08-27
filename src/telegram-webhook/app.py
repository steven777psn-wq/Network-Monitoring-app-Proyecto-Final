from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/alert", methods=["POST"])
def alert():
    data = request.json
    alerts = data.get("alerts", [])
    for alert in alerts:
        name = alert["labels"].get("alertname", "Sin nombre")
        description = alert["annotations"].get("description", "Sin descripción")
        severity = alert["labels"].get("severity", "Sin severidad")
        message = f"🚨 *{name}*\n📄 {description}\n⚠️ *Severity:* {severity}"
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        )
    return "OK", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)