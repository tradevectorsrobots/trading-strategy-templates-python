"""
Bollinger Bands Strategy for NSE/BSE India
Trade Vectors | https://tradevectors.com

Strategy Logic:
- Buy when price touches or crosses below the Lower Bollinger Band
- Sell when price touches or crosses above the Upper Bollinger Band
- Middle Band (SMA) acts as a reference / exit level

Compatible with: Zerodha Kite Connect, Upstox API
Data Source: yfinance (Yahoo Finance)
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
SYMBOL = "TCS.NS"             # NSE symbol (.NS for NSE, .BO for BSE)
START_DATE = "2023-01-01"
END_DATE = "2024-12-31"
BB_PERIOD = 20                # Rolling window for SMA and std dev
BB_STD = 2.0                  # Number of standard deviations for bands
INITIAL_CAPITAL = 100000      # Starting capital in INR
# ──────────────────────────────────────────────────────────────────────────────


def fetch_data(symbol, start, end):
    """Fetch OHLCV data from Yahoo Finance."""
    df = yf.download(symbol, start=start, end=end, auto_adjust=True)
    if df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")
    df.index = pd.to_datetime(df.index)
    return df


def compute_bollinger_bands(df, period, num_std):
    """Compute Bollinger Bands and %B indicator."""
    df = df.copy()
    df["BB_Middle"] = df["Close"].rolling(window=period).mean()
    rolling_std = df["Close"].rolling(window=period).std()
    df["BB_Upper"] = df["BB_Middle"] + (num_std * rolling_std)
    df["BB_Lower"] = df["BB_Middle"] - (num_std * rolling_std)
    df["BB_Pct"] = (df["Close"] - df["BB_Lower"]) / (df["BB_Upper"] - df["BB_Lower"])
    df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / df["BB_Middle"]
    return df


def compute_signals(df):
    """Generate buy/sell signals based on Bollinger Band touches."""
    df = df.copy()
    df["Below_Lower"] = (df["Close"] < df["BB_Lower"]).astype(int)
    df["Above_Upper"] = (df["Close"] > df["BB_Upper"]).astype(int)
    df["Buy_Signal"] = df["Below_Lower"].diff().clip(lower=0)
    df["Sell_Signal"] = df["Above_Upper"].diff().clip(lower=0)
    return df


def backtest(df, initial_capital):
    """Run a simple backtest on Bollinger Band signals."""
    df = df.copy()
    position = 0
    capital = initial_capital
    shares = 0
    portfolio_values = []

    for _, row in df.iterrows():
        price = row["Close"]
        if row["Buy_Signal"] == 1 and capital > 0:
            shares = capital // price
            capital -= shares * price
            position = 1
        elif row["Sell_Signal"] == 1 and position == 1:
            capital += shares * price
            shares = 0
            position = 0
        portfolio_values.append(capital + shares * price)

    df["Portfolio_Value"] = portfolio_values
    return df


def print_performance(df, initial_capital):
    """Print strategy performance metrics."""
    final_value = df["Portfolio_Value"].iloc[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    buy_hold_return = ((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100

    print("\n" + "=" * 45)
    print(" BOLLINGER BANDS STRATEGY — PERFORMANCE")
    print("=" * 45)
    print(f" Symbol          : {SYMBOL}")
    print(f" Period          : {START_DATE} to {END_DATE}")
    print(f" BB Period       : {BB_PERIOD}")
    print(f" BB Std Dev      : {BB_STD}")
    print(f" Buy Signals     : {int(df['Buy_Signal'].sum())}")
    print(f" Sell Signals    : {int(df['Sell_Signal'].sum())}")
    print(f" Initial Capital : ₹{initial_capital:,.2f}")
    print(f" Final Value     : ₹{final_value:,.2f}")
    print(f" Strategy Return : {total_return:.2f}%")
    print(f" Buy & Hold      : {buy_hold_return:.2f}%")
    print("=" * 45)


def plot_strategy(df):
    """Plot price with Bollinger Bands, %B, and portfolio value."""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True,
                                         gridspec_kw={"height_ratios": [3, 1.5, 1.5]})

    ax1.plot(df.index, df["Close"], label="Close Price", color="steelblue", linewidth=1.5)
    ax1.plot(df.index, df["BB_Upper"], label="Upper Band", color="red", linewidth=1, linestyle="--")
    ax1.plot(df.index, df["BB_Middle"], label=f"Middle Band (SMA {BB_PERIOD})", color="orange", linewidth=1)
    ax1.plot(df.index, df["BB_Lower"], label="Lower Band", color="green", linewidth=1, linestyle="--")
    ax1.fill_between(df.index, df["BB_Lower"], df["BB_Upper"], alpha=0.05, color="gray")

    buy_signals = df[df["Buy_Signal"] == 1]
    sell_signals = df[df["Sell_Signal"] == 1]
    ax1.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="lime", s=100, label="Buy", zorder=5)
    ax1.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red", s=100, label="Sell", zorder=5)
    ax1.set_title(f"Bollinger Bands Strategy — {SYMBOL}", fontsize=14)
    ax1.set_ylabel("Price (INR)")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(df.index, df["BB_Pct"], label="%B", color="purple", linewidth=1.2)
    ax2.axhline(1.0, color="red", linestyle="--", linewidth=1, label="Overbought (1.0)")
    ax2.axhline(0.0, color="green", linestyle="--", linewidth=1, label="Oversold (0.0)")
    ax2.set_ylabel("%B")
    ax2.legend()
    ax2.grid(alpha=0.3)

    ax3.plot(df.index, df["Portfolio_Value"], color="purple", linewidth=1.5)
    ax3.set_title("Portfolio Value Over Time")
    ax3.set_ylabel("Value (INR)")
    ax3.set_xlabel("Date")
    ax3.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("bollinger_bands_strategy.png", dpi=150)
    plt.show()
    print("Chart saved as bollinger_bands_strategy.png")


if __name__ == "__main__":
    data = fetch_data(SYMBOL, START_DATE, END_DATE)
    data = compute_bollinger_bands(data, BB_PERIOD, BB_STD)
    data = compute_signals(data)
    data = backtest(data, INITIAL_CAPITAL)
    print_performance(data, INITIAL_CAPITAL)
    plot_strategy(data)

# ─── LIVE TRADING INTEGRATION (Zerodha Kite Connect) ─────────────────────────
# Replace fetch_data() with real-time Kite Connect API calls.
# Visit https://tradevectors.com for live trading setup guides.
# ─────────────────────────────────────────────────────────────────────────────
