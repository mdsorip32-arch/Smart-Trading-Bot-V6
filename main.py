import telebot
import ccxt
import pandas as pd
import pandas_ta as ta
import time
import os
import pytz
from datetime import datetime

TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance() 
SYMBOL = 'BTC/USDT'
SAUDI_TZ = pytz.timezone('Asia/Riyadh')

def get_saudi_time():
    return datetime.now(SAUDI_TZ).strftime('%I:%M:%S %p')

def start_smart_trading():
    bot.send_message(USER_ID, "🛡️ স্মার্ট এনালাইজার সক্রিয়! আমি প্রতি ৬০ সেকেন্ডে আপনাকে আপডেট দেব।")
    while True:
        try:
            bars = exchange.fetch_ohlcv(SYMBOL, timeframe='1m', limit=30)
            df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
            
            # এনালাইসিস ক্যালকুলেশন
            df['RSI'] = ta.rsi(df['close'], length=14)
            df['EMA'] = ta.ema(df['close'], length=10)
            last = df.iloc[-1]
            
            # লজিক এবং সিগন্যাল জেনারেশন
            if last['close'] > last['EMA'] and last['RSI'] < 70:
                decision = "🟢 **PREDICTION: UP** 🟢\n🚀 মার্কেট বুলিশ! ১ মিনিটের ট্রেড নিন।"
            elif last['close'] < last['EMA'] and last['RSI'] > 30:
                decision = "🔴 **PREDICTION: DOWN** 🔴\n📉 মার্কেট বিয়ারিশ! ১ মিনিটের ট্রেড নিন।"
            else:
                decision = "⏳ **HOLD / NEUTRAL** ⏳\n⚠️ মার্কেট এখন রিস্কি, ট্রেড এড়িয়ে চলুন।"

            # প্রতি মিনিটেই আপডেট পাঠানো নিশ্চিত করা
            msg = (f"🎯 **POCKET OPTION SMART BOT**\n"
                   f"🕒 Time: {get_saudi_time()}\n"
                   f"💹 Asset: {SYMBOL}\n\n"
                   f"📢 **{decision}**\n\n"
                   f"💰 Live Price: {last['close']}\n"
                   f"📊 RSI: {round(last['RSI'], 2)}")
            
            bot.send_message(USER_ID, msg, parse_mode='Markdown')
            time.sleep(60)
            
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    start_smart_trading()
