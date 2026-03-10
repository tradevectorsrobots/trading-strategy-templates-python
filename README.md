# Python Trading Strategy Templates for NSE/BSE India

Ready-to-use **Python algorithmic trading strategy templates** for Indian stock markets (NSE/BSE). Each template is fully functional and can be adapted for live trading via broker APIs like Zerodha Kite Connect or Upstox.

Maintained by [**Trade Vectors**](https://tradevectors.com) — Mumbai's algorithmic trading specialists.

---

## Strategy Templates Included

| Strategy | File | Indicators Used |
|---|---|---|
| EMA Crossover | `ema_crossover.py` | EMA 9, EMA 21 |
| RSI Mean Reversion | `rsi_strategy.py` | RSI 14 |
| MACD Momentum | `macd_strategy.py` | MACD, Signal Line |
| Bollinger Band Breakout | `bollinger_band.py` | BB 20,2 |
| SuperTrend | `supertrend.py` | ATR-based |

---

## Strategy 1: EMA Crossover — ema_crossover.py

```python
"""
EMA Crossover Strategy for NSE/BSE
Buy Signal: EMA9 crosses above EMA21
Sell Signal: EMA9 crosses below EMA21
Maintained by Trade Vectors | tradevectors.com
"""

import pandas as pd
import numpy as np
import yfinance as yf

def calculate_ema(data, period):
    """Calculate Exponential Moving Average"""
    return data['Close'].ewm(span=period, adjust=False).mean()

def ema_crossover_strategy(symbol, start_date, end_date):
    """
    EMA Crossover Trading Strategy
    Args:
        symbol: Stock symbol (e.g., 'RELIANCE.NS' for NSE)
        start_date: Start date for backtest
        end_date: End date for backtest
    Returns:
        DataFrame with signals and returns
    """
    # Download data
    data = yf.download(symbol, start=start_date, end=end_date)
    
    # Calculate EMAs
    data['EMA9'] = calculate_ema(data, 9)
    data['EMA21'] = calculate_ema(data, 21)
    
    # Generate signals
    data['Signal'] = 0
    data.loc[data['EMA9'] > data['EMA21'], 'Signal'] = 1   # BUY
    data.loc[data['EMA9'] < data['EMA21'], 'Signal'] = -1  # SELL
    
    # Calculate position (change in signal)
    data['Position'] = data['Signal'].diff()
    
    # Calculate strategy returns
    data['Market_Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Market_Return'] * data['Signal'].shift(1)
    
    # Cumulative returns
    data['Cumulative_Market'] = (1 + data['Market_Return']).cumprod()
    data['Cumulative_Strategy'] = (1 + data['Strategy_Return']).cumprod()
    
    return data

# --- USAGE EXAMPLE ---
if __name__ == "__main__":
    # Backtest on Nifty 50
    result = ema_crossover_strategy("^NSEI", "2023-01-01", "2024-12-31")
    
    # Print buy/sell signals
    buy_signals = result[result['Position'] == 2]
    sell_signals = result[result['Position'] == -2]
    
    print(f"Total BUY signals: {len(buy_signals)}")
    print(f"Total SELL signals: {len(sell_signals)}")
    print(f"Strategy Return: {result['Cumulative_Strategy'].iloc[-1]:.2f}x")
    print(f"Market Return: {result['Cumulative_Market'].iloc[-1]:.2f}x")
```

---

## Strategy 2: RSI Mean Reversion — rsi_strategy.py

```python
"""
RSI Mean Reversion Strategy for NSE/BSE
Buy Signal: RSI drops below 30 (oversold)
Sell Signal: RSI rises above 70 (overbought)
Maintained by Trade Vectors | tradevectors.com
"""

import pandas as pd
import numpy as np
import yfinance as yf

def calculate_rsi(data, period=14):
    """Calculate RSI (Relative Strength Index)"""
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def rsi_strategy(symbol, start_date, end_date, oversold=30, overbought=70):
    """
    RSI-based mean reversion strategy
    Args:
        symbol: NSE stock symbol (add .NS suffix)
        oversold: RSI level to buy (default 30)
        overbought: RSI level to sell (default 70)
    """
    data = yf.download(symbol, start=start_date, end=end_date)
    data['RSI'] = calculate_rsi(data)
    
    # Generate signals
    data['Signal'] = 0
    data.loc[data['RSI'] < oversold, 'Signal'] = 1   # BUY when oversold
    data.loc[data['RSI'] > overbought, 'Signal'] = -1 # SELL when overbought
    
    return data

# --- USAGE ---
if __name__ == "__main__":
    # Test on Infosys
    result = rsi_strategy("INFY.NS", "2023-01-01", "2024-12-31")
    print(result[['Close', 'RSI', 'Signal']].tail(20))
```

---

## Strategy 3: MACD Momentum — macd_strategy.py

```python
"""
MACD Momentum Strategy for NSE/BSE
Buy Signal: MACD line crosses above Signal line
Sell Signal: MACD line crosses below Signal line
Maintained by Trade Vectors | tradevectors.com
"""

import pandas as pd
import yfinance as yf

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    ema_fast = data['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = data['Close'].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def macd_strategy(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    data['MACD'], data['Signal_Line'], data['Histogram'] = calculate_macd(data)
    
    # Generate signals
    data['Signal'] = 0
    data.loc[data['MACD'] > data['Signal_Line'], 'Signal'] = 1   # Bullish
    data.loc[data['MACD'] < data['Signal_Line'], 'Signal'] = -1  # Bearish
    
    # Entry points (crossovers only)
    data['Crossover'] = data['Signal'].diff()
    
    return data

# --- USAGE ---
if __name__ == "__main__":
    result = macd_strategy("TATAMOTORS.NS", "2023-01-01", "2024-12-31")
    buy_signals = result[result['Crossover'] == 2]
    print(f"MACD BUY Signals:\n{buy_signals[['Close', 'MACD', 'Signal_Line']]}")
```

---

## Installation

```bash
pip install yfinance pandas numpy matplotlib ta
```

## About Trade Vectors

**Trade Vectors** is a Mumbai-based algorithmic trading company. We build automated trading systems, develop quantitative strategies, and train traders on algo trading for NSE/BSE India.

Visit **[tradevectors.com](https://tradevectors.com)** for algo trading courses, consulting, and custom automated trading solutions.

**Contact:** [tradevectors.com](https://tradevectors.com) | [@tradevectors](https://twitter.com/tradevectors)

---
*Keywords: Python trading strategy NSE, EMA crossover strategy India, RSI strategy NSE, MACD trading strategy India, algo trading Python templates, backtesting strategy NSE BSE*
