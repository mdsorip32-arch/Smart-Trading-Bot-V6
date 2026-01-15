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
    bot.send_message(USER_ID, f"🚀 ট্রেডিং বট সিগন্যাল দেওয়া শুরু করছে...\nসময়: {get_saudi_time()}")
    while True:
        try:
            # ২. দ্রুত ডাটা ফেচিং
            ticker = exchange.fetch_ticker(SYMBOL)
            price = ticker['last']
            open_price = ticker['open']
            
            # ৩. সরল মুভমেন্ট লজিক (যাতে প্রতি মিনিটে সিগন্যাল আসে)
            if price > open_price:
                status = "🟢 **PREDICTION: UP** 🟢"
                instruction = "🚀 মার্কেট উপরের দিকে! ১ মিনিটের জন্য UP ট্রেড নিন।"
            elif price < open_price:
                status = "🔴 **PREDICTION: DOWN** 🔴"
                instruction = "📉 মার্কেট নিচের দিকে! ১ মিনিটের জন্য DOWN ট্রেড নিন।"
            else:
                status = "⏳ **MARKET STABLE** ⏳"
                instruction = "⚠️ মার্কেট এখন স্থির, পরের ক্যান্ডেল দেখুন।"

            # ৪. সিগন্যাল মেসেজ
            msg = (
                f"🎯 **POCKET OPTION SIGNAL**\n"
                f"🕒 Time (KSA): {get_saudi_time()}\n"
                f"💹 Asset: {SYMBOL}\n\n"
                f"📢 **Decision: {status}**\n\n"
                f"📝 {instruction}\n"
                f"💰 Live Price: {price}"
            )
            bot.send_message(USER_ID, msg, parse_mode='Markdown')
            
            # ৫. ঠিক ৬০ সেকেন্ড পর পর আপডেট
            time.sleep(60)
            
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    start_trading()
