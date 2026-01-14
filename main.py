import telebot
import yfinance as yf
import pandas_ta as ta
import mplfinance as mpf
import time
import os

# আপনার টোকেন এবং আইডি (Render/Environment Variable থেকে আসবে)
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)

# যে মার্কেটে সিগন্যাল চান
SYMBOLS = ['GC=F', 'BTC-USD', 'EURUSD=X'] 

def check_market():
    for symbol in SYMBOLS:
        try:
            # ৫ মিনিটের লাইভ ডাটা ডাউনলোড
            df = yf.download(symbol, interval='5m', period='1d', progress=False)
            if df.empty: continue

            # RSI ইন্ডিকেটর (মার্কেট মুভমেন্ট বোঝার জন্য)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            last_row = df.iloc[-1]
            
            # সিগন্যাল লজিক: যেকোনো জায়গায় শর্ত মিললেই ট্রেড নিবে
            if last_row['RSI'] < 35:
                send_signal(symbol, df, "BUY")
            elif last_row['RSI'] > 65:
                send_signal(symbol, df, "SELL")
                
        except Exception as e:
            print(f"Error: {e}")

def send_signal(symbol, df, side):
    entry_price = float(df['Close'].iloc[-1])
    
    # আপনার ৩০০ পয়েন্টের হিসাব (১০০ পয়েন্ট লস : ২০০ পয়েন্ট লাভ)
    if side == "BUY":
        stop_loss = entry_price - 100
        take_profit = entry_price + 200
    else:
        stop_loss = entry_price + 100
        take_profit = entry_price - 200
    
    chart_filename = f"{symbol}_chart.png"
    # চার্টে শেষ ক্যান্ডেলগুলো দেখাবে
    mpf.plot(df.tail(30), type='candle', style='charles', savefig=chart_filename)

    caption = (
        f"🚨 **NEW SIGNAL: {symbol}** 🚨\n\n"
        f"📈 **Action:** {side}\n"
        f"💰 **Entry Price:** {round(entry_price, 2)}\n"
        f"🛑 **Stop Loss (SL):** {round(stop_loss, 2)} (-100 pts)\n"
        f"🎯 **Target (TP): {round(take_profit, 2)}** (+200 pts)\n\n"
        f"📏 **Total Range:** 300 Points Setup"
    )
    
    with open(chart_filename, 'rb') as photo:
        bot.send_photo(USER_ID, photo, caption=caption, parse_mode='Markdown')
    os.remove(chart_filename)

if __name__ == "__main__":
    bot.send_message(USER_ID, "🚀 ৩০০ পয়েন্ট রেঞ্জ বোট চালু হয়েছে! যেকোনো পজিশনে সিগন্যাল দিবে।")
    while True:
        check_market()
        time.sleep(300) # ৫ মিনিট পর পর মার্কেট চেক করবে
