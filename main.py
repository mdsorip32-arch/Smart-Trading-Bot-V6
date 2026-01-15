import telebot
import ccxt
import pandas as pd
import pandas_ta as ta
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

def get_signal():
    try:
        # ২. মার্কেট ডাটা সংগ্রহ (এনালাইসিসের জন্য ৩০টি ক্যান্ডেল)
        bars = exchange.fetch_ohlcv(SYMBOL, timeframe='1m', limit=30)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
        
        # ৩. টেকনিক্যাল এনালাইসিস (ক্যালকুলেশন)
        # RSI ক্যালকুলেশন (মার্কেট কি খুব উপরে নাকি খুব নিচে তা বুঝবে)
        df['RSI'] = ta.rsi(df['close'], length=14)
        # EMA (মার্কেট ট্রেন্ড বোঝার জন্য)
        df['EMA'] = ta.ema(df['close'], length=10)
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        # ৪. বুদ্ধিমত্তার সাথে সিদ্ধান্ত গ্রহণ (Logic)
        # যদি RSI ৩০ এর নিচে থাকে (Oversold) এবং দাম বাড়ছে - UP সিগন্যাল
        if last['close'] > last['EMA'] and last['RSI'] < 70:
            status = "🟢 **PREDICTION: UP** 🟢"
            logic = "Analysis: Market is Bullish (EMA Support)"
        # যদি RSI ৭০ এর উপরে থাকে (Overbought) এবং দাম কমছে - DOWN সিগন্যাল
        elif last['close'] < last['EMA'] and last['RSI'] > 30:
            status = "🔴 **PREDICTION: DOWN** 🔴"
            logic = "Analysis: Market is Bearish (EMA Resistance)"
        else:
            status = "⏳ **WAITING** ⏳"
            logic = "Analysis: Market is Sideways. No safe trade."

        # ৫. সিগন্যাল পাঠানো
        msg = (f"🎯 **SMART ANALYZER**\n"
               f"🕒 Time: {get_saudi_time()}\n"
               f"💹 Asset: {SYMBOL}\n"
               f"📊 {logic}\n\n"
               f"📢 **Decision: {status}**\n"
               f"💰 Live Price: {last['close']}")
        
        bot.send_message(USER_ID, msg, parse_mode='Markdown')

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bot.send_message(USER_ID, "✅ এনালাইসিস মোড চালু হয়েছে। বট এখন মার্কেট ক্যালকুলেশন করছে...")
    while True:
        get_signal()
        time.sleep(60) # প্রতি ১ মিনিটে একটি নিখুঁত এনালাইসিস
