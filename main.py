import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_URL = "https://api.telegram.org/bot" + str(TELEGRAM_TOKEN)

def get_updates(offset=None):
    r = requests.get(TELEGRAM_URL + "/getUpdates", params={"timeout": 30, "offset": offset})
    return r.json()

def send_message(chat_id, text):
    requests.post(TELEGRAM_URL + "/sendMessage", data={"chat_id": chat_id, "text": str(text)[:4000]})

def ask_gemini(msg):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    r = requests.post(url, json={"contents": [{"parts": [{"text": msg}]}]})
    data = r.json()
    if "candidates" in data:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    return str(data)

offset = None
print("Bot iniciado!")
while True:
    for update in get_updates(offset).get("result", []):
        offset = update["update_id"] + 1
        msg = update.get("message", {})
        chat_id = msg.get("chat", {}).get("id")
        text = msg.get("text", "")
        if text and chat_id:
            try:
                send_message(chat_id, ask_gemini(text))
            except Exception as e:
                send_message(chat_id, str(e))
                print(e)
