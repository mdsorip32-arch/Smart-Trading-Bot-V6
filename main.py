import telebot
import ccxt
import pandas_ta as ta
import time
import os
import pytz
from datetime import datetime
import pandas as pd

TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance() 
SYMBOL = 'BTC/USDT'
SAUDI_TZ = pytz.timezone('Asia/Riyadh')

def get_saudi_time():
    return datetime.now(SAUDI_TZ).strftime('%I:%M:%S %p')

def get_live_signal():
    while True:
        try:
            bars = exchange.fetch_ohlcv(SYMBOL, timeframe='1m', limit=30)
            df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['RSI'] = ta.rsi(df['close'], length=3)
            last_row = df.iloc[-1]
            
            if last_row['close'] > last_row['open']:
                status = "🟢 **PREDICTION: UP** 🟢"
                instruction = "🚀 ১ মিনিটের জন্য UP ট্রেড নিন!"
            elif last_row['close'] < last_row['open']:
                status = "🔴 **PREDICTION: DOWN** 🔴"
                instruction = "📉 ১ মিনিটের জন্য DOWN ট্রেড নিন!"
            else:
                status = "⏳ **WAITING** ⏳"
                instruction = "⚠️ মার্কেট অস্থির, পরের ক্যান্ডেল দেখুন।"

            msg = (f"🎯 **LIVE MARKET SIGNAL**\n"
                   f"🕒 Time (KSA): {get_saudi_time()}\n"
                   f"💹 Asset: {SYMBOL}\n\n"
                   f"📢 **Decision: {status}**\n\n"
                   f"📝 {instruction}\n"
                   f"💰 Live Price: {last_row['close']}")
            bot.send_message(USER_ID, msg, parse_mode='Markdown')
            time.sleep(60)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    bot.send_message(USER_ID, "✅ পকেট অপশন লাইভ ডাটা বট সক্রিয়!")
    get_live_signal()
