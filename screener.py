# screener.py

import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime
import pytz
from dhan_config import DHAN_API_KEY, DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN
from fetch_fno_symbols import get_fno_symbols

HEADERS = {
    "access-token": DHAN_ACCESS_TOKEN,
    "client-id": DHAN_CLIENT_ID
}

BASE_URL = "https://api.dhan.co"

def fetch_30min_data(symbol):
    url = f"{BASE_URL}/chart/intraday/{symbol}/NSE/30M"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠️ Error fetching data for {symbol}: {response.text}")
        return None
    data = response.json().get('data', [])
    df = pd.DataFrame(data)
    if df.empty:
        return None
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df = df.rename(columns={"open": "o", "high": "h", "low": "l", "close": "c", "volume": "v"})
    df = df[['time', 'o', 'h', 'l', 'c', 'v']]
    return df

def calculate_ema(series, period=20):
    return series.ewm(span=period, adjust=False).mean()

def is_mother_candle(row):
    range_ = row['h'] - row['l']
    return range_ > row['atr']  # use ATR as dynamic threshold

def check_pattern(df):
    if len(df) < 30:
        return False

    df['atr'] = df['h'].rolling(14).max() - df['l'].rolling(14).min()
    df['ema20'] = calculate_ema(df['c'], 20)

    m = df.iloc[-6]
    b1, b2, b3, b4 = df.iloc[-5], df.iloc[-4], df.iloc[-3], df.iloc[-2]

    if not is_mother_candle(m):
        return False
    if not (m['v'] > b1['v'] > b2['v'] > b3['v'] > b4['v']):
        return False

    for baby in [b1, b2, b3, b4]:
        if not (baby['h'] < m['h'] and baby['l'] > m['l']):
            return False

    if not (b4['c'] > df.iloc[-2]['ema20']):
        return False

    return True

def is_market_open_ist():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    is_weekday = now.weekday() < 5  # Mon-Fri
    market_open = now.hour > 9 or (now.hour == 9 and now.minute >= 15)
    market_close = now.hour < 15 or (now.hour == 15 and now.minute <= 30)
    return is_weekday and market_open and market_close

def main():
    if not is_market_open_ist():
        print("⏳ Market is closed. Screener runs only Mon–Fri, 09:15–15:30 IST.")
        return

    symbols = get_fno_symbols()
    print(f"\n📦 Scanning {len(symbols)} F&O stocks...\n")

    for i, symbol in enumerate(symbols):
        df = fetch_30min_data(symbol)
        if df is not None and check_pattern(df):
            print(f"✅ Pattern detected in {symbol}")
        else:
            print(f"❌ No pattern in {symbol}")
        time.sleep(0.4)

if __name__ == "__main__":
    main()
