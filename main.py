import telebot
import yfinance as yf
import pandas_ta as ta
import time
import os
import pytz
from datetime import datetime

# ১. কানেকশন (Render থেকে নিবে)
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)
SYMBOL = 'BTC-USD' 

# ২. সৌদি আরব টাইমজোন (KSA)
SAUDI_TZ = pytz.timezone('Asia/Riyadh')

def get_saudi_time():
    return datetime.now(SAUDI_TZ).strftime('%I:%M:%S %p')

def start_active_bot():
    while True:
        try:
            # ৩. লাইভ মার্কেট ডাটা
            ticker = yf.Ticker(SYMBOL)
            df = ticker.history(period="1d", interval="1m")
            
            if not df.empty and len(df) > 10:
                # ৪. ফাস্ট এনালাইসিস (RSI পিরিয়ড ৫ করা হয়েছে দ্রুত সিগন্যালের জন্য)
                df['RSI'] = ta.rsi(df['Close'], length=5) 
                last_row = df.iloc[-1]
                
                # ৫. সিগন্যাল লজিক (যাতে আপনি বেশি ট্রেড পান)
                # ক্যান্ডেল উপরে ক্লোজ হলে এবং RSI ৭০ এর নিচে থাকলে UP
                if last_row['Close'] > last_row['Open'] and last_row['RSI'] < 75:
                    status = "🟢 **PREDICTION: UP** 🟢"
                    instruction = "🚀 ট্রেন্ড পজিটিভ! ১ মিনিটের জন্য UP ট্রেড নিন।"
                
                # ক্যান্ডেল নিচে ক্লোজ হলে এবং RSI ৩০ এর উপরে থাকলে DOWN
                elif last_row['Close'] < last_row['Open'] and last_row['RSI'] > 25:
                    status = "🔴 **PREDICTION: DOWN** 🔴"
                    instruction = "📉 ট্রেন্ড নেগেটিভ! ১ মিনিটের জন্য DOWN ট্রেড নিন।"
                
                else:
                    status = "⏳ **HOLD / WAIT** ⏳"
                    instruction = "⚠️ মার্কেট এখন স্থির, পরের ক্যান্ডেল দেখুন।"

                # ৬. সরাসরি সিগন্যাল মেসেজ
                msg = (
                    f"🎯 **FAST-ACTION SIGNAL (1 MIN)**\n"
                    f"🕒 Time (KSA): {get_saudi_time()}\n"
                    f"💹 Asset: {SYMBOL}\n\n"
                    f"📢 **Decision: {status}**\n\n"
                    f"📝 {instruction}\n"
                    f"💰 Live Price: {round(last_row['Close'], 2)}"
                )
                bot.send_message(USER_ID, msg, parse_mode='Markdown')

            # ৭. ঠিক ৬০ সেকেন্ড পর পর আপডেট
            time.sleep(60) 
            
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    bot.send_message(USER_ID, f"✅ একটিভ ট্রেডিং বট চালু হয়েছে!\nএখন থেকে আপনি দ্রুত সিগন্যাল পাবেন।\nসময়: {get_saudi_time()}")
    start_active_bot()
                
