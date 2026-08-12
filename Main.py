import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# جلب البيانات من إعدادات Render بشكل آمن
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_alert(data):
    ticker = data.get("ticker", "N/A")
    price = data.get("close", "N/A")
    event = data.get("event", "تنبيه مضارب")
    msg_detail = data.get("message", "")
    time_str = data.get("time", "")

    text = f"""
🎯 <b>تنبيه من مؤشر المضارب المكتمل v3.2</b>
━────━━━━────━
📊 <b>السهم:</b> <code>{ticker}</code>
💰 <b>السعر:</b> <code>{price}</code>
⚡ <b>نوع الإشارة:</b> {event}

📝 <b>التفاصيل:</b>
{msg_detail}

⏰ <i>الوقت: {time_str}</i>
━────━━━━────━
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        send_telegram_alert(data)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
