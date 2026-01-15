import telebot
import ccxt
import time
import os
import pytz
from datetime import datetime

# ===== CONFIG =====
TOKEN = os.getenv("TOKEN")
USER_ID = int(os.getenv("USER_ID"))

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# ✅ Bybit (Binance নয়)
exchange = ccxt.bybit({
    "enableRateLimit": True
})

SYMBOL = "BTC/USDT"
SAUDI_TZ = pytz.timezone("Asia/Riyadh")

def saudi_time():
    return datetime.now(SAUDI_TZ).strftime("%I:%M:%S %p")

bot.send_message(USER_ID, "✅ লাইভ ১-মিনিট BTC সিগন্যাল চালু হয়েছে")

while True:
    try:
        # ১-মিনিট ক্যান্ডেল
        ohlcv = exchange.fetch_ohlcv(SYMBOL, timeframe="1m", limit=2)

        prev = ohlcv[-2]
        curr = ohlcv[-1]

        open_price = curr[1]
        close_price = curr[4]

        if close_price > open_price:
            signal = "🟢 **UP** → BUY"
        elif close_price < open_price:
            signal = "🔴 **DOWN** → SELL"
        else:
            signal = "⏸ **HOLD**"

        msg = (
            f"📊 **BTC 1-MIN SIGNAL**\n"
            f"🕒 {saudi_time()}\n\n"
            f"{signal}\n"
            f"💰 Price: `{close_price}`"
        )

        bot.send_message(USER_ID, msg)
        time.sleep(60)

    except Exception as e:
        bot.send_message(USER_ID, f"⚠️ Error: `{e}`")
        time.sleep(30)
