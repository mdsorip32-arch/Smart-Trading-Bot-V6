import telebot
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
import time
import os

# Render Environment Variables
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)

SYMBOLS = ['GC=F', 'BTC-USD', 'EURUSD=X'] 

def check_market():
    for symbol in SYMBOLS:
        try:
            # ১৫ মিনিটের ডাটা ডাউনলোড (আপনি চাইলে '30m' বা '5m' করতে পারেন)
            df = yf.download(symbol, interval='15m', period='2d', progress=False)
            if df.empty: continue

            # ইন্ডিকেটর
            df['EMA_20'] = ta.ema(df['Close'], length=20)
            df['EMA_50'] = ta.ema(df['Close'], length=50)
            df.ta.rsi(append=True)
            
            last_row = df.iloc[-1]
            prev_row = df.iloc[-2]
            
            # সিগন্যাল লজিক (EMA Cross)
            if (prev_row['EMA_20'] < prev_row['EMA_50']) and (last_row['EMA_20'] > last_row['EMA_50']):
                create_chart_and_send(symbol, df, "BUY")
                
        except Exception as e:
            print(f"Error: {e}")

def create_chart_and_send(symbol, df, side):
    # শেষ ৩০টি ক্যান্ডেল চার্টে দেখাবে
    df_plot = df.tail(30).copy()
    
    price = float(df_plot['Close'].iloc[-1])
    # ক্যান্ডেল অনুযায়ী স্টপ লস (শেষ ২ ক্যান্ডেলের লো এর নিচে)
    stop_loss = float(df_plot['Low'].iloc[-2:].min() * 0.999) 
    take_profit = float(price + (price - stop_loss) * 2) # ১:২ রিস্ক রিওয়ার্ড

    # চার্টে লাইন যোগ করা (SL, TP, Entry)
    lines = [
        mpf.make_addplot([price]*len(df_plot), color='blue', linestyle='--'),   # Entry
        mpf.make_addplot([stop_loss]*len(df_plot), color='red', linestyle='-'), # SL
        mpf.make_addplot([take_profit]*len(df_plot), color='green', linestyle='-') # TP
    ]

    chart_filename = f"{symbol}_chart.png"
    
    # ক্যান্ডেলস্টিক চার্ট তৈরি
    mpf.plot(df_plot, type='candle', style='charles', 
             title=f"{symbol} {side} Signal",
             ylabel='Price',
             addplot=lines,
             savefig=chart_filename)

    # টেলিগ্রামে ছবি ও ডিটেইলস পাঠানো
    caption = (
        f"🚨 **NEW SIGNAL: {symbol}** 🚨\n\n"
        f"📈 **Action:** {side}\n"
        f"💰 **Entry:** {round(price, 2)}\n"
        f"🛑 **Stop Loss:** {round(stop_loss, 2)}\n"
        f"🎯 **Target (TP): {round(take_profit, 2)}**\n\n"
        f"📊 *Chart: 15m Candles with SL/TP lines*"
    )
    
    with open(chart_filename, 'rb') as photo:
        bot.send_photo(USER_ID, photo, caption=caption, parse_mode='Markdown')
    
    os.remove(chart_filename) # ছবি পাঠিয়ে ডিলিট করে দেওয়া

if __name__ == "__main__":
    bot.send_message(USER_ID, "🚀 Automatic Candle Scanner Started!")
    while True:
        check_market()
        time.sleep(300)
                # ৩০ মিনিট পর পর মেসেজ পাঠানোর লজিক
        if int(time.time()) % 1800 < 300:
            bot.send_message(USER_ID, "✅ আপনি বর্তমানে অ্যাক্টিভ রয়েছেন।")
            
        
