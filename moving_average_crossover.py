"""
Moving Average Crossover Strategy for NSE/BSE India
Trade Vectors | https://tradevectors.com

Strategy Logic:
- Buy when the short-term SMA crosses above the long-term SMA (Golden Cross)
- Sell when the short-term SMA crosses below the long-term SMA (Death Cross)

Compatible with: Zerodha Kite Connect, Upstox API
Data Source: yfinance (Yahoo Finance)
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
SYMBOL = "RELIANCE.NS"       # NSE symbol (append .NS for NSE, .BO for BSE)
START_DATE = "2023-01-01"
END_DATE = "2024-12-31"
SHORT_WINDOW = 20             # Short-term SMA period
LONG_WINDOW = 50              # Long-term SMA period
INITIAL_CAPITAL = 100000      # Starting capital in INR
# ──────────────────────────────────────────────────────────────────────────────


def fetch_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Fetch OHLCV data from Yahoo Finance."""
    print(f"Fetching data for {symbol} from {start} to {end}...")
    df = yf.download(symbol, start=start, end=end, auto_adjust=True)
    if df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")
    df.index = pd.to_datetime(df.index)
    print(f"Downloaded {len(df)} trading days.")
    return df


def compute_signals(df: pd.DataFrame, short_window: int, long_window: int) -> pd.DataFrame:
    """Compute SMA indicators and generate buy/sell signals."""
    df = df.copy()
    df["SMA_Short"] = df["Close"].rolling(window=short_window, min_periods=1).mean()
    df["SMA_Long"] = df["Close"].rolling(window=long_window, min_periods=1).mean()

    # Signal: 1 = long (hold), 0 = no position
    df["Signal"] = 0
    df.loc[df["SMA_Short"] > df["SMA_Long"], "Signal"] = 1

    # Crossover events: 1 = buy, -1 = sell
    df["Crossover"] = df["Signal"].diff()
    return df


def backtest(df: pd.DataFrame, initial_capital: float) -> pd.DataFrame:
    """Run a simple backtest on the crossover signals."""
    df = df.copy()
    position = 0
    capital = initial_capital
    shares = 0
    portfolio_values = []

    for _, row in df.iterrows():
        price = row["Close"]
        if row["Crossover"] == 1 and capital > 0:   # Buy signal
            shares = capital // price
            capital -= shares * price
            position = 1
        elif row["Crossover"] == -1 and position == 1:  # Sell signal
            capital += shares * price
            shares = 0
            position = 0
        portfolio_values.append(capital + shares * price)

    df["Portfolio_Value"] = portfolio_values
    return df


def print_performance(df: pd.DataFrame, initial_capital: float) -> None:
    """Print strategy performance metrics."""
    final_value = df["Portfolio_Value"].iloc[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    buy_hold_return = ((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100

    print("\n" + "=" * 45)
    print(" MOVING AVERAGE CROSSOVER — PERFORMANCE")
    print("=" * 45)
    print(f" Symbol          : {SYMBOL}")
    print(f" Period          : {START_DATE} to {END_DATE}")
    print(f" Short SMA       : {SHORT_WINDOW} days")
    print(f" Long SMA        : {LONG_WINDOW} days")
    print(f" Initial Capital : ₹{initial_capital:,.2f}")
    print(f" Final Value     : ₹{final_value:,.2f}")
    print(f" Strategy Return : {total_return:.2f}%")
    print(f" Buy & Hold      : {buy_hold_return:.2f}%")
    print("=" * 45)


def plot_strategy(df: pd.DataFrame) -> None:
    """Plot price, SMAs, buy/sell signals, and portfolio value."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    ax1.plot(df.index, df["Close"], label="Close Price", color="steelblue", linewidth=1.5)
    ax1.plot(df.index, df["SMA_Short"], label=f"SMA {SHORT_WINDOW}", color="orange", linewidth=1.2)
    ax1.plot(df.index, df["SMA_Long"], label=f"SMA {LONG_WINDOW}", color="green", linewidth=1.2)

    buy_signals = df[df["Crossover"] == 1]
    sell_signals = df[df["Crossover"] == -1]
    ax1.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="lime", s=100, label="Buy", zorder=5)
    ax1.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red", s=100, label="Sell", zorder=5)

    ax1.set_title(f"MA Crossover Strategy — {SYMBOL}", fontsize=14)
    ax1.set_ylabel("Price (INR)")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(df.index, df["Portfolio_Value"], color="purple", linewidth=1.5)
    ax2.set_title("Portfolio Value Over Time")
    ax2.set_ylabel("Value (INR)")
    ax2.set_xlabel("Date")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("ma_crossover_strategy.png", dpi=150)
    plt.show()
    print("Chart saved as ma_crossover_strategy.png")


if __name__ == "__main__":
    # 1. Fetch data
    data = fetch_data(SYMBOL, START_DATE, END_DATE)

    # 2. Compute signals
    data = compute_signals(data, SHORT_WINDOW, LONG_WINDOW)

    # 3. Backtest
    data = backtest(data, INITIAL_CAPITAL)

    # 4. Performance report
    print_performance(data, INITIAL_CAPITAL)

    # 5. Plot
    plot_strategy(data)

    # 6. Show buy/sell signal dates
    print("\nBuy signals:")
    print(data[data["Crossover"] == 1][["Close", "SMA_Short", "SMA_Long"]].to_string())
    print("\nSell signals:")
    print(data[data["Crossover"] == -1][["Close", "SMA_Short", "SMA_Long"]].to_string())

# ─── LIVE TRADING INTEGRATION (Zerodha Kite Connect) ─────────────────────────
# To use with live data, replace fetch_data() with:
#
#   from kiteconnect import KiteConnect
#   kite = KiteConnect(api_key="YOUR_API_KEY")
#   kite.set_access_token("YOUR_ACCESS_TOKEN")
#   data = kite.historical_data(instrument_token, from_date, to_date, "day")
#
# Visit https://tradevectors.com for Kite Connect integration guides.
# ─────────────────────────────────────────────────────────────────────────────
