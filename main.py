import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PAIR_URL = "https://api.dexscreener.com/latest/dex/tokens/0xc5b21abce2f0c7f3d445fd80bf8f5aa98d3e9b5a"

TIMEFRAME = 15 * 60

THRESHOLD_LONG = 1.015
THRESHOLD_SHORT = 0.985

last_price = None
last_signal = None

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except:
        pass

def get_price():
    try:
        r = requests.get(PAIR_URL).json()
        return float(r["pairs"][0]["priceUsd"])
    except:
        return None

while True:
    price = get_price()

    if price is None:
        time.sleep(10)
        continue

    if last_price is None:
        last_price = price
        time.sleep(10)
        continue

    change = price / last_price

    if change >= THRESHOLD_LONG and last_signal != "LONG":
        entry = price
        tp = entry * 1.02
        sl = entry * 0.985

        send_telegram(
            f"🚀 LONG SIGNAL\nEntry: {entry:.6f}\nTP: {tp:.6f}\nSL: {sl:.6f}"
        )
        last_signal = "LONG"

    if change <= THRESHOLD_SHORT and last_signal != "SHORT":
        entry = price
        tp = entry * 0.98
        sl = entry * 1.015

        send_telegram(
            f"📉 SHORT SIGNAL\nEntry: {entry:.6f}\nTP: {tp:.6f}\nSL: {sl:.6f}"
        )
        last_signal = "SHORT"

    last_price = price

    time.sleep(10)
