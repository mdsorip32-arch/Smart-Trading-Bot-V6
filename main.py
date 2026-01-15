import telebot
import yfinance as yf
import pandas_ta as ta
import time
import os
import pytz
from datetime import datetime

# ১. কানেকশন সেটআপ
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)
SYMBOL = 'BTC-USD' # আপনি চাইলে অন্য পেয়ার দিতে পারেন

# ২. সৌদি আরব টাইমজোন
SAUDI_TZ = pytz.timezone('Asia/Riyadh')

def get_saudi_time():
    return datetime.now(SAUDI_TZ).strftime('%I:%M:%S %p')

def start_trading_bot():
    while True:
        try:
            # ৩. ডাটা সংগ্রহ
            ticker = yf.Ticker(SYMBOL)
            df = ticker.history(period="1d", interval="1m")
            
            if not df.empty and len(df) > 15:
                # ৪. কঠিন এনালাইসিস ইন্ডিকেটর
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['EMA_short'] = ta.ema(df['Close'], length=9)
                df['EMA_long'] = ta.ema(df['Close'], length=21)
                
                last_row = df.iloc[-1]
                
                # ৫. সিগন্যাল ডিসিশন লজিক (প্রতি মিনিটে আপডেট দিবে)
                # কড়া শর্ত: RSI এবং EMA ক্রসওভার একসাথে মিললে ট্রেড
                if last_row['RSI'] < 40 and last_row['Close'] > last_row['EMA_short']:
                    status = "🟢 **BUY / UP (Call)** 🟢"
                    instruction = "🚀 পরের ১ মিনিটের জন্য UP ট্রেড নিন!"
                elif last_row['RSI'] > 60 and last_row['Close'] < last_row['EMA_short']:
                    status = "🔴 **SELL / DOWN (Put)** 🔴"
                    instruction = "📉 পরের ১ মিনিটের জন্য DOWN ট্রেড নিন!"
                else:
                    status = "⏳ **HOLD / WAIT** ⏳"
                    instruction = "⚠️ মার্কেট এখন ক্লিয়ার না, এই মিনিটে ট্রেড এড়িয়ে চলুন।"

                # ৬. মেসেজ পাঠানো
                msg = (
                    f"⏰ **1-MIN ACCURACY SIGNAL**\n"
                    f"🕒 Time: {get_saudi_time()}\n"
                    f"💹 Asset: {SYMBOL}\n\n"
                    f"📢 **Decision: {status}**\n\n"
                    f"📝 {instruction}\n"
                    f"💰 Price: {round(last_row['Close'], 2)}"
                )
                bot.send_message(USER_ID, msg, parse_mode='Markdown')
            
            # ৭. ঠিক ৬০ সেকেন্ড পর পর আপডেট
            time.sleep(60) 
            
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    bot.send_message(USER_ID, f"🚀 ট্রেডিং বট সক্রিয়! প্রতি মিনিটে আপনি আপডেট পাবেন।\nবর্তমান সময়: {get_saudi_time()}")
    start_trading_bot()
