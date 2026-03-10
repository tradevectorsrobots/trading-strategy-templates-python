"""
MACD (Moving Average Convergence Divergence) Strategy for NSE/BSE India
Trade Vectors | https://tradevectors.com

Strategy Logic:
- Buy when MACD line crosses above the Signal line (bullish crossover)
- Sell when MACD line crosses below the Signal line (bearish crossover)
- Optional histogram filter: only trade when histogram confirms direction

Compatible with: Zerodha Kite Connect, Upstox API
Data Source: yfinance (Yahoo Finance)
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
SYMBOL = "HDFCBANK.NS"        # NSE symbol (.NS for NSE, .BO for BSE)
START_DATE = "2023-01-01"
END_DATE = "2024-12-31"
FAST_PERIOD = 12              # Fast EMA period
SLOW_PERIOD = 26             # Slow EMA period
SIGNAL_PERIOD = 9            # Signal line EMA period
INITIAL_CAPITAL = 100000     # Starting capital in INR
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


def compute_macd(df: pd.DataFrame, fast: int, slow: int, signal: int) -> pd.DataFrame:
    """Compute MACD line, Signal line, and Histogram."""
    df = df.copy()
    ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()

    df["MACD"] = ema_fast - ema_slow
    df["Signal_Line"] = df["MACD"].ewm(span=signal, adjust=False).mean()
    df["Histogram"] = df["MACD"] - df["Signal_Line"]
    return df


def compute_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Generate buy/sell signals based on MACD crossover."""
    df = df.copy()

    # 1 when MACD above Signal, 0 when below
    df["Position"] = np.where(df["MACD"] > df["Signal_Line"], 1, 0)

    # Detect crossover: +1 = bullish (buy), -1 = bearish (sell)
    df["Crossover"] = df["Position"].diff()
    return df


def backtest(df: pd.DataFrame, initial_capital: float) -> pd.DataFrame:
    """Run a simple backtest on MACD crossover signals."""
    df = df.copy()
    position = 0
    capital = initial_capital
    shares = 0
    portfolio_values = []

    for _, row in df.iterrows():
        price = row["Close"]
        if row["Crossover"] == 1 and capital > 0:    # Buy signal
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

    buy_trades = len(df[df["Crossover"] == 1])
    sell_trades = len(df[df["Crossover"] == -1])

    print("\n" + "=" * 45)
    print(" MACD STRATEGY — PERFORMANCE")
    print("=" * 45)
    print(f" Symbol          : {SYMBOL}")
    print(f" Period          : {START_DATE} to {END_DATE}")
    print(f" MACD            : {FAST_PERIOD}/{SLOW_PERIOD}/{SIGNAL_PERIOD}")
    print(f" Buy Signals     : {buy_trades}")
    print(f" Sell Signals    : {sell_trades}")
    print(f" Initial Capital : ₹{initial_capital:,.2f}")
    print(f" Final Value     : ₹{final_value:,.2f}")
    print(f" Strategy Return : {total_return:.2f}%")
    print(f" Buy & Hold      : {buy_hold_return:.2f}%")
    print("=" * 45)


def plot_strategy(df: pd.DataFrame) -> None:
    """Plot price chart, MACD indicator, and portfolio value."""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True,
                                         gridspec_kw={"height_ratios": [3, 2, 1.5]})

    # Price chart with signals
    ax1.plot(df.index, df["Close"], label="Close Price", color="steelblue", linewidth=1.5)
    buy_signals = df[df["Crossover"] == 1]
    sell_signals = df[df["Crossover"] == -1]
    ax1.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="lime", s=100, label="Buy", zorder=5)
    ax1.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red", s=100, label="Sell", zorder=5)
    ax1.set_title(f"MACD Strategy — {SYMBOL}", fontsize=14)
    ax1.set_ylabel("Price (INR)")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # MACD chart
    ax2.plot(df.index, df["MACD"], label="MACD", color="blue", linewidth=1.2)
    ax2.plot(df.index, df["Signal_Line"], label="Signal Line", color="orange", linewidth=1.2)
    colors = ["green" if h >= 0 else "red" for h in df["Histogram"]]
    ax2.bar(df.index, df["Histogram"], label="Histogram", color=colors, alpha=0.5)
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax2.set_ylabel("MACD")
    ax2.legend()
    ax2.grid(alpha=0.3)

    # Portfolio value
    ax3.plot(df.index, df["Portfolio_Value"], color="purple", linewidth=1.5)
    ax3.set_title("Portfolio Value Over Time")
    ax3.set_ylabel("Value (INR)")
    ax3.set_xlabel("Date")
    ax3.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("macd_strategy.png", dpi=150)
    plt.show()
    print("Chart saved as macd_strategy.png")


if __name__ == "__main__":
    data = fetch_data(SYMBOL, START_DATE, END_DATE)
    data = compute_macd(data, FAST_PERIOD, SLOW_PERIOD, SIGNAL_PERIOD)
    data = compute_signals(data)
    data = backtest(data, INITIAL_CAPITAL)
    print_performance(data, INITIAL_CAPITAL)
    plot_strategy(data)

    print("\nBuy signals (MACD crossover above Signal):")
    print(data[data["Crossover"] == 1][["Close", "MACD", "Signal_Line"]].to_string())
    print("\nSell signals (MACD crossover below Signal):")
    print(data[data["Crossover"] == -1][["Close", "MACD", "Signal_Line"]].to_string())

# ─── LIVE TRADING INTEGRATION (Zerodha Kite Connect) ─────────────────────────
# Replace fetch_data() with real-time Kite Connect API calls.
# Visit https://tradevectors.com for live trading setup guides.
# ─────────────────────────────────────────────────────────────────────────────
