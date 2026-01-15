import telebot
import ccxt
import time
import os
import pytz
from datetime import datetime

# ১. কানেকশন
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance() 
SYMBOL = 'BTC/USDT'
SAUDI_TZ = pytz.timezone('Asia/Riyadh')

def get_saudi_time():
    return datetime.now(SAUDI_TZ).strftime('%I:%M:%S %p')

def start_trading():
    # বট চালু হওয়া মাত্র মেসেজ দিবে
    bot.send_message(USER_ID, "✅ লাইভ সিগন্যাল সার্ভিস শুরু হয়েছে! প্রতি মিনিটে আপডেট পাবেন।")
    
    while True:
        try:
            # ২. দ্রুত লাইভ ডাটা (এনালাইসিস সহ)
            ticker = exchange.fetch_ticker(SYMBOL)
            price = ticker['last']
            open_price = ticker['open']
            
            # ৩. এনালাইসিস লজিক
            if price > open_price:
                res = "🟢 **PREDICTION: UP** 🟢\n🚀 ১ মিনিটের জন্য BUY ট্রেড নিন।"
            elif price < open_price:
                res = "🔴 **PREDICTION: DOWN** 🔴\n📉 ১ মিনিটের জন্য SELL ট্রেড নিন।"
            else:
                res = "⏳ **HOLD** ⏳\n⚠️ মার্কেট স্থির আছে।"

            # ৪. মেসেজ পাঠানো
            msg = (f"🎯 **POCKET OPTION SIGNAL**\n"
                   f"🕒 Time: {get_saudi_time()}\n"
                   f"💹 Asset: {SYMBOL}\n\n"
                   f"📢 {res}\n\n"
                   f"💰 Price: {price}")
            
            bot.send_message(USER_ID, msg, parse_mode='Markdown')
            
            # ঠিক ৬০ সেকেন্ড বিরতি
            time.sleep(60)

        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    start_trading()
            
