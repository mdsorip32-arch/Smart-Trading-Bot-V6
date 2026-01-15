import telebot
import yfinance as yf
import pandas_ta as ta
import time
import os

# ১. টোকেন ও আইডি কানেকশন
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)

# ২. মার্কেট সিলেক্ট (BTC বা EURUSD)
SYMBOL = 'BTC-USD' 

def binary_style_signal():
    while True:
        try:
            # ৩. ১ মিনিটের ক্যান্ডেল ডাটা ডাউনলোড
            df = yf.download(SYMBOL, interval='1m', period='1d', progress=False)
            if not df.empty:
                # ৪. ক্যান্ডেলের মুভমেন্ট ও RSI এনালাইসিস
                df['RSI'] = ta.rsi(df['Close'], length=14)
                last_row = df.iloc[-1]
                
                # ৫. আপনার ১-মিনিটের লাভের জন্য লজিক (৫ সেকেন্ডের ভিডিওর মতো)
                if last_row['Close'] > last_row['Open'] or last_row['RSI'] < 50:
                    direction = "🟢 **PREDICTION: UP** 🟢\n🚀 পরের ১ মিনিট উপরে থাকবে!"
                else:
                    direction = "🔴 **PREDICTION: DOWN** 🔴\n📉 পরের ১ মিনিট নিচে নামবে!"

                # ৬. সরাসরি সিগন্যাল মেসেজ
                msg = (
                    f"⏰ **1 MINUTE TRADE SIGNAL**\n"
                    f"💹 Asset: {SYMBOL}\n\n"
                    f"{direction}\n\n"
                    f"💵 ১ মিনিটের জন্য ট্রেড নিন!"
                )
                bot.send_message(USER_ID, msg, parse_mode='Markdown')

            # ৭. ঠিক ৬০ সেকেন্ড পর পর নতুন ক্যান্ডেল সিগন্যাল
            time.sleep(60) 
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    bot.send_message(USER_ID, "✅ ১-মিনিট প্রফিট বট চালু হয়েছে!\nএখন থেকে প্রতি মিনিটে সিগন্যাল পাবেন।")
    binary_style_signal()
