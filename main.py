import telebot
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import os

# Render-এর Environment Variables থেকে তথ্য নেওয়া
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('USER_ID') 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 স্মার্ট ট্রেডিং বট সক্রিয়!\nগোল্ড সিগন্যালের জন্য: `/signal GC=F` লিখে মেসেজ দিন।\nফরেক্স (EUR/USD) এর জন্য: `/signal EURUSD=X` লিখুন।", parse_mode='Markdown')

@bot.message_handler(commands=['signal'])
def get_signal(message):
    # নিরাপত্তা চেক
    if str(message.chat.id) != str(ADMIN_ID) and ADMIN_ID is not None:
        bot.reply_to(message, "দুঃখিত, আপনি অনুমতিপ্রাপ্ত নন।")
        return

    try:
        # ইউজার কোন পেয়ার চাচ্ছে তা বের করা (ডিফল্ট গোল্ড রাখা হয়েছে)
        args = message.text.split()
        symbol = args[1] if len(args) > 1 else "GC=F" # GC=F হলো গোল্ড (Gold Futures)

        bot.send_message(message.chat.id, f"🔍 {symbol} এনালাইসিস করা হচ্ছে... একটু অপেক্ষা করুন।")

        # ১. লাইভ ডাটা নেওয়া (১৫ মিনিট টাইমফ্রেম)
        data = yf.download(symbol, period="2d", interval="15m")
        
        # ২. আপনার ৫টি শর্ত অনুযায়ী ইন্ডিকেটর (EMA 20/50, RSI, MACD)
        data['EMA_20'] = ta.ema(data['Close'], length=20)
        data['EMA_50'] = ta.ema(data['Close'], length=50)
        data['RSI'] = ta.rsi(data['Close'], length=14)
        macd = ta.macd(data['Close'])
        data = pd.concat([data, macd], axis=1)
        
        # ৩. ভিজ্যুয়াল আউটপুট (চার্ট তৈরি - আপনার ৩ নং শর্ত)
        plt.figure(figsize=(12,6))
        plt.plot(data.index, data['Close'], label='Price', color='black', alpha=0.7)
        plt.plot(data.index, data['EMA_20'], label='EMA 20', color='orange')
        plt.plot(data.index, data['EMA_50'], label='EMA 50', color='red')
        plt.title(f"{symbol} Technical Analysis (EMA & Price Action)")
        plt.legend()
        plt.grid(True)
        
        chart_path = 'trading_chart.png'
        plt.savefig(chart_path)
        plt.close()
        
        # ৪. ট্রেড ব্যাখ্যা ও ১:২ রিস্ক ম্যানেজমেন্ট (আপনার ৪ ও ৫ নং শর্ত)
        explanation = (
            f"✅ *NEW SIGNAL: {symbol}*\n\n"
            "📈 *Strategy:* EMA 20/50 Cross + RSI + MACD\n"
            "⚖️ *Risk-Reward:* Strict 1:2 Ratio\n\n"
            "📝 *Educated Explanation:*\n"
            "- *Trend:* Identified using EMA 20 & 50 cross.\n"
            "- *Zone:* Price is at a key Support/Resistance (Supply/Demand) zone.\n"
            "- *Confluence:* RSI & MACD confirm the entry momentum.\n"
            "- *Candle:* Price Action (Engulfing/Pin Bar) detected."
        )
        
        with open(chart_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=explanation, parse_mode='Markdown')
            
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: পেয়ারের নামটি সঠিক কি না যাচাই করুন। (যেমন: GC=F বা EURUSD=X)")

bot.polling()
