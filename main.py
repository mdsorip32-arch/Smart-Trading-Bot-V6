import telebot
import yfinance as yf
import pandas_ta as ta
import time
import os

# ১. কানেকশন
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)

# ২. আপনার পছন্দের পেয়ার (ভিডিওর মতো EUR/USD বা BTC)
SYMBOL = 'BTC-USD' 

def send_signal():
    while True:
        try:
            # ৩. ১ মিনিটের ডাটা নেওয়া
            df = yf.download(SYMBOL, interval='1m', period='1d', progress=False)
            if not df.empty:
                # ৪. এনালাইসিস (RSI এবং ক্যান্ডেল মুভমেন্ট)
                df['RSI'] = ta.rsi(df['Close'], length=14)
                last_row = df.iloc[-1]
                
                # ৫. ভিডিওর মতো সরাসরি সিগন্যাল লজিক
                if last_row['RSI'] < 45:
                    direction = "🟢 **Your Signal is UP** 🟢\n🚀 পরবর্তী ১ মিনিট উপরে যাবে!"
                elif last_row['RSI'] > 55:
                    direction = "🔴 **Your Signal is DOWN** 🔴\n📉 পরবর্তী ১ মিনিট নিচে যাবে!"
                else:
                    direction = "⏳ **WAITING** ⏳\nমার্কেট এখন স্থির, পরের বার দেখুন।"

                # ৬. ভিডিওর স্টাইলে মেসেজ
                msg = (
                    f"✨ **ADVANCED TRADING SIGNAL** ✨\n\n"
                    f"💹 Pair: {SYMBOL}\n"
                    f"⏰ Timeframe: 1 Minute\n\n"
                    f"{direction}\n\n"
                    f"💰 Current Price: {round(last_row['Close'], 2)}"
                )
                bot.send_message(USER_ID, msg, parse_mode='Markdown')

            # ৭. ঠিক ১ মিনিট অপেক্ষা
            time.sleep(60) 
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    bot.send_message(USER_ID, "✅ আপনার ১-মিনিট সিগন্যাল বট এখন সক্রিয়!\nভিডিওর মতো সিগন্যাল পেতে থাকুন।")
    send_signal()
