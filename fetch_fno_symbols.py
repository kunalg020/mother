# fetch_fno_symbols.py

import requests
import pandas as pd

def get_fno_symbols():
    url = "https://www.nseindia.com/api/liveEquity-derivatives"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    }

    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)  # set cookie
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Failed to fetch F&O symbols from NSE")
        return []

    data = response.json()
    df = pd.DataFrame(data['data'])
    symbols = df['underlying'].dropna().unique().tolist()
    return sorted(list(set(symbols)))
