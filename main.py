import telebot
import ccxt
import time
import os
import pytz
from datetime import datetime

# ১. কানেকশন সেটআপ
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance() 
SYMBOL = 'BTC/USDT'
SAUDI_TZ = pytz.timezone('Asia/Riyadh')

def get_saudi_time():
    return datetime.now(SAUDI_TZ).strftime('%I:%M:%S %p')

def send_signal():
    try:
        # ২. দ্রুত লাইভ প্রাইস সংগ্রহ
        ticker = exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        open_price = ticker['open']
        
        # ৩. খুব সহজ লজিক (যাতে প্রতি মিনিটে সিগন্যাল পান)
        if price > open_price:
            status = "🟢 **PREDICTION: UP** 🟢"
            decision = "🚀 ১ মিনিটের জন্য BUY ট্রেড নিন!"
        elif price < open_price:
            status = "🔴 **PREDICTION: DOWN** 🔴"
            decision = "📉 ১ মিনিটের জন্য SELL ট্রেড নিন!"
        else:
            status = "⏳ **WAITING** ⏳"
            decision = "⚠️ মার্কেট এখন স্থির।"

        # ৪. সিগন্যাল মেসেজ
        msg = (
            f"🎯 **POCKET OPTION LIVE**\n"
            f"🕒 Time: {get_saudi_time()}\n"
            f"💹 Pair: {SYMBOL}\n\n"
            f"📢 **Decision: {status}**\n"
            f"📝 {decision}\n\n"
            f"💰 Price: {price}"
        )
        bot.send_message(USER_ID, msg, parse_mode='Markdown')
        print(f"Signal sent at {get_saudi_time()}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bot.send_message(USER_ID, "✅ বট এখন ১০০% একটিভ। প্রতি মিনিটে সিগন্যাল আসবে।")
    while True:
        send_signal()
        # ৫. বিরতি কমিয়ে ৬০ সেকেন্ডের বদলে ৩০ সেকেন্ড করা হলো যাতে কানেকশন না কাটে
        time.sleep(30) 
