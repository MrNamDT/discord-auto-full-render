import os
import time
import requests
from flask import Flask
import threading

# === Flask giữ port để Render không tắt service ===
app = Flask(__name__)

@app.route('/')
def index():
    return "🚀 Bot is running on Render!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_web).start()
# ==================================================

# === Script gửi tin nhắn ===
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    print("❌ Thiếu TOKEN hoặc CHANNEL_ID trong biến môi trường!")
    exit(1)

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def send_message():
    url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
    payload = {
        "content": "."
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} ✅ Gửi thành công")
        elif response.status_code == 401:
            print("❌ Token không hợp lệ (401 Unauthorized)")
        elif response.status_code == 403:
            print("❌ Không có quyền gửi tin nhắn (403 Forbidden)")
        elif response.status_code == 404:
            print("❌ Channel ID sai hoặc không tồn tại (404)")
        elif response.status_code == 429:
            retry = response.json().get("retry_after", 10)
            print(f"⚠️ Rate limited. Chờ {retry}s...")
            time.sleep(float(retry))
        else:
            print(f"⚠️ Lỗi {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Lỗi gửi tin nhắn: {e}")

if __name__ == "__main__":
    print("▶️ Bắt đầu gửi tin nhắn mỗi 2 giờ...")
    while True:
        send_message()
        time.sleep(20)