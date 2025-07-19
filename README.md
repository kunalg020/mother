# 📈 Mother Candle Screener with Dhan API (30-min TF)

This script scans for a bullish Mother Candle pattern using Dhan API on 30-minute timeframe.

## ✅ Pattern Rules
- 1 large Mother Candle (high volume, wide range)
- Followed by 4 Baby Candles:
  - Entirely inside the mother candle
  - Each with decreasing volume
- Last candle closes above the 20 EMA (bullish filter)

## 🔧 Setup

1. Clone the repo:
   ```
   git clone https://github.com/<your-username>/mother-candle-screener.git
   cd mother-candle-screener
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Add your Dhan API credentials to `dhan_config.py`.

4. Run the screener:
   ```
   python screener.py
   ```

## 🕒 Market Time Restriction

This screener only runs on weekdays between 09:15 and 15:30 IST.

## 🔄 Dynamic F&O Support

This screener auto-fetches the current NSE F&O stock list from:
https://www.nseindia.com/api/liveEquity-derivatives
