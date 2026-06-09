import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
TELEGRAM_URL = "https://api.telegram.org/bot" + str(TELEGRAM_TOKEN)

def get_updates(offset=None):
    r = requests.get(TELEGRAM_URL + "/getUpdates", params={"timeout": 30, "offset": offset})
    return r.json()

def send_message(chat_id, text):
    requests.post(TELEGRAM_URL + "/sendMessage", data={"chat_id": chat_id, "text": text})

def ask_claude(msg):
    r = requests.post("https://api.anthropic.com/v1/messages", json={"model": "claude-sonnet-4-20250514", "max_tokens": 1000, "messages": [{"role": "user", "content": msg}]}, headers={"Content-Type": "application/json", "x-api-key": ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01"})
    return r.json()["content"][0]["text"]

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
                send_message(chat_id, ask_claude(text))
            except Exception as e:
                send_message(chat_id, "Erro!")
                print(e)
