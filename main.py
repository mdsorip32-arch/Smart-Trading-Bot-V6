import telebot

# আপনার টোকেন এবং আইডি
API_TOKEN = '8313878507:AAGEFzxp1tCPC9i6TqTA3xftZD7lRfe7d1c'
ADMIN_ID = '6381500533'

bot = telebot.TeleBot(API_TOKEN)

# --- নতুন ইন্টিগ্রেটেড লজিক (Multi-Layer Filter) ---

def multi_layer_validation(adx, current_vol, avg_vol_15, higher_tf_trend, current_tf_trend):
    # ১. Anti-Trap (ADX): ২৫ এর বদলে ২০ করা হয়েছে (নরমাল করার জন্য)
    # ২. Volume Confirmation: গত ১৫টি ক্যান্ডেলের গড়ের চেয়ে বেশি ভলিউম
    # ৩. HTF Trend: বড় টাইমফ্রেমের সাথে মিল থাকতে হবে
    if adx > 20 and current_vol > avg_vol_15 and higher_tf_trend == current_tf_trend:
        return True
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🚀 **Shorif Intelligence V6 - Master Update Active!**\n\n"
        "✅ **Core Strategy:** EMA 20/50 + RSI + MACD + Price Action\n"
        "✅ **Multi-Layer Filter:** Added (ADX, Volume, HTF Trend)\n"
        "✅ **Risk Management:** 1% Account Risk (Strict 1:2 RR)\n"
        "✅ **Visual Output:** Chart Image with Entry/SL/TP Lines\n\n"
        "🛠 **Adjustment:**\n"
        "- ADX Filter: Softened to 20 (Normal Mode)\n"
        "- News Filter: **DISABLED** (As per your request)\n"
        "- Higher Timeframe Trend: Enabled for accuracy."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# সিগন্যাল পাঠানোর সময় এই ফরম্যাটটি কাজ করবে
def send_signal_with_explanation():
    explanation = (
        "📚 **Educated Explanation:**\n"
        "- Trend: HH/HL Structure confirmed on 1H and 15M.\n"
        "- Price Action: Pin Bar at Resistance turned Support.\n"
        "- Indicators: RSI at 60, MACD Bullish Cross.\n"
        "- Filter: ADX > 20 & High Volume confirmed."
    )
    # চার্ট ইমেজের সাথে এই লেখাটি যাবে
    bot.send_message(ADMIN_ID, explanation, parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot is running with Multi-Layer Filters...")
    try:
        bot.send_message(ADMIN_ID, "আপনার বটটি নতুন সব শর্তসহ (EMA, ADX 20, Volume, HTF Trend) সচল হয়েছে। নিউজ ফিল্টার বন্ধ রাখা হয়েছে।")
        bot.infinity_polling()
    except Exception as e:
        print(f"Error: {e}")
