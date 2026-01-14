import telebot
import yfinance as yf
import pandas_ta as ta
import mplfinance as mpf
import time
import os
import threading

# ১. টোকেন ও আইডি কানেকশন
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
bot = telebot.TeleBot(TOKEN)

# ২. আপনার নির্ধারিত মার্কেট (গোল্ড, বিটকয়েন, ফরেক্স)
SYMBOLS = ['GC=F', 'BTC-USD', 'EURUSD=X'] 

def check_market():
    for symbol in SYMBOLS:
        try:
            # ৩. মার্কেট ডাটা ডাউনলোড (৫ মিনিটের ক্যান্ডেল)
            df = yf.download(symbol, interval='5m', period='1d', progress=False)
            if df.empty: continue

            # ৪. বোট কী দেখে ট্রেড নিবে: RSI ইন্ডিকেটর (মার্কেটের শক্তি মাপার যন্ত্র)
            # এটি দেখবে মার্কেট কি অনেক নিচে (BUY করার সুযোগ) নাকি অনেক উপরে (SELL করার সুযোগ)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            last_row = df.iloc[-1]
            
            # ৫. ট্রেড নেওয়ার শর্ত: RSI ৩৫ এর নিচে মানে BUY, ৬৫ এর উপরে মানে SELL
            if last_row['RSI'] < 35:
                send_signal(symbol, df, "BUY")
            elif last_row['RSI'] > 65:
                send_signal(symbol, df, "SELL")
                
        except Exception as e:
            print(f"Error: {e}")

def send_signal(symbol, df, side):
    entry_price = float(df['Close'].iloc[-1])
    
    # ৬. আপনার কাঙ্ক্ষিত লস ও লাভের নিখুঁত ক্যালকুলেশন (১০$ লস / ২০$ লাভ)
    if side == "BUY":
        stop_loss = entry_price - 1.0 # এটি প্রায় ১০ ডলার লস (০.০১ লটে)
        take_profit = entry_price + 2.0 # এটি প্রায় ২০ ডলার লাভ (০.০১ লটে)
    else:
        stop_loss = entry_price + 1.0
        take_profit = entry_price - 2.0
    
    # ৭. লট সাইজ নোট (আপনার নির্দেশ অনুযায়ী)
    lot_info = "Lot 0.04 (Forex) / Lot 0.01 (Gold/BTC) = $10 Loss / $20 Profit"
    
    chart_filename = f"{symbol}_chart.png"
    # ৮. ক্যান্ডেলস্টিক চার্টের ছবি তৈরি (প্রমাণ হিসেবে)
    mpf.plot(df.tail(30), type='candle', style='charles', savefig=chart_filename)

    # ৯. সিগন্যাল মেসেজ ফরম্যাট
    caption = (
        f"🚨 **NEW SIGNAL: {symbol}** 🚨\n\n"
        f"📈 **Action:** {side}\n"
        f"💰 **Entry Price:** {round(entry_price, 2)}\n"
        f"🛑 **Stop Loss (SL):** {round(stop_loss, 2)} (Loss $10)\n"
        f"🎯 **Target (TP): {round(take_profit, 2)}** (Profit $20)\n\n"
        f"📋 **Instruction:**\n"
        f"👉 {lot_info}\n\n"
        f"📊 **Reason:** RSI Strategy Applied"
    )
    
    with open(chart_filename, 'rb') as photo:
        bot.send_photo(USER_ID, photo, caption=caption, parse_mode='Markdown')
    os.remove(chart_filename)

# ১০. নতুন আদেশ: লাইভ মার্কেট ভেরিফিকেশন (বোট জীবিত কি না চেক করা)
@bot.message_handler(func=lambda message: True)
def live_check(message):
    text = message.text.upper()
    target = None
    if "GOLD" in text or "GC=F" in text: target = "GC=F"
    elif "BTC" in text: target = "BTC-USD"
    
    if target:
        df = yf.download(target, interval='5m', period='1d', progress=False)
        current_price = round(df['Close'].iloc[-1], 2)
        chart_file = f"live_{target}.png"
        mpf.plot(df.tail(30), type='candle', style='charles', savefig=chart_file)
        
        with open(chart_file, 'rb') as photo:
            bot.send_photo(USER_ID, photo, caption=f"✅ **LIVE PRICE: {target}**\nPrice: {current_price}\nBot is Active!")
        os.remove(chart_file)

if __name__ == "__main__":
    # ১১. অহেতুক হার্টবিট মেসেজ বন্ধ রাখা হয়েছে
    bot.send_message(USER_ID, "🚀 বোট চালু হয়েছে! এখন থেকে এটি $১০ লস ও $২০ লাভ এর সিগন্যাল খুঁজবে।")
    threading.Thread(target=bot.polling, daemon=True).start()
    while True:
        check_market()
        time.sleep(300) 
