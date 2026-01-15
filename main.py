import telebot
import ccxt
import time
import os
import pytz
import threading
from datetime import datetime

# ===== CONFIG =====
TOKEN = os.getenv("TOKEN")
USER_ID = int(os.getenv("USER_ID"))

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
exchange = ccxt.binance({"enableRateLimit": True})
SYMBOL = "BTC/USDT"
SAUDI_TZ = pytz.timezone("Asia/Riyadh")

trading_active = False

def get_saudi_time():
    return datetime.now(SAUDI_TZ).strftime('%I:%M:%S %p')

def trading_loop():
    global trading_active

    bot.send_message(USER_ID, "✅ লাইভ BTC সিগন্যাল শুরু হয়েছে")

    while trading_active:
        try:
            ticker = exchange.fetch_ticker(SYMBOL)
            price = ticker["last"]
            open_price = ticker["open"]

            if price > open_price:
                res = "🟢 *BUY* (১ মিনিট)"
            elif price < open_price:
                res = "🔴 *SELL* (১ মিনিট)"
            else:
                res = "⏸ *HOLD*"

            msg = (
                f"📊 *BTC SIGNAL*\n"
                f"🕒 {get_saudi_time()}\n"
                f"💹 {SYMBOL}\n\n"
                f"{res}\n"
                f"💰 Price: `{price}`"
            )

            bot.send_message(USER_ID, msg)
            time.sleep(60)

        except Exception as e:
            bot.send_message(USER_ID, f"⚠️ Error: `{e}`")
            time.sleep(15)

@bot.message_handler(commands=["start"])
def start(message):
    global trading_active

    if trading_active:
        bot.reply_to(message, "⚠️ ট্রেডিং আগেই চালু আছে")
        return

    trading_active = True
    threading.Thread(target=trading_loop).start()
    bot.reply_to(message, "🚀 ট্রেডিং চালু করা হয়েছে")

@bot.message_handler(commands=["stop"])
def stop(message):
    global trading_active
    trading_active = False
    bot.reply_to(message, "⛔ ট্রেডিং বন্ধ করা হয়েছে")

# ===== BOT RUN =====
bot.infinity_polling()
