"""
RSI (Relative Strength Index) Strategy for NSE/BSE India
Trade Vectors | https://tradevectors.com

Strategy Logic:
- Buy when RSI crosses below the oversold threshold (default: 30)
- Sell when RSI crosses above the overbought threshold (default: 70)

Compatible with: Zerodha Kite Connect, Upstox API
Data Source: yfinance (Yahoo Finance)
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
SYMBOL = "INFY.NS"            # NSE symbol (.NS for NSE, .BO for BSE)
START_DATE = "2023-01-01"
END_DATE = "2024-12-31"
RSI_PERIOD = 14               # Lookback period for RSI calculation
OVERSOLD = 30                 # RSI level considered oversold (buy zone)
OVERBOUGHT = 70              # RSI level considered overbought (sell zone)
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


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculate RSI using Wilder's smoothing method."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_signals(df: pd.DataFrame, period: int, oversold: int, overbought: int) -> pd.DataFrame:
    """Compute RSI and generate buy/sell signals."""
    df = df.copy()
    df["RSI"] = compute_rsi(df["Close"], period)

    # Generate signals based on RSI thresholds
    df["Signal"] = 0
    df.loc[df["RSI"] < oversold, "Signal"] = 1   # Oversold -> potential buy
    df.loc[df["RSI"] > overbought, "Signal"] = -1 # Overbought -> potential sell

    # Detect crossover events (avoid repeated signals in same zone)
    df["Position"] = df["Signal"].replace(0, np.nan).ffill().fillna(0)
    df["Trade"] = df["Position"].diff()
    return df


def backtest(df: pd.DataFrame, initial_capital: float) -> pd.DataFrame:
    """Run a simple backtest on RSI signals."""
    df = df.copy()
    position = 0
    capital = initial_capital
    shares = 0
    portfolio_values = []

    for _, row in df.iterrows():
        price = row["Close"]
        if row["Trade"] > 0 and capital > 0:    # Buy signal
            shares = capital // price
            capital -= shares * price
            position = 1
        elif row["Trade"] < 0 and position == 1:  # Sell signal
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
    print(" RSI STRATEGY — PERFORMANCE")
    print("=" * 45)
    print(f" Symbol          : {SYMBOL}")
    print(f" Period          : {START_DATE} to {END_DATE}")
    print(f" RSI Period      : {RSI_PERIOD}")
    print(f" Oversold Level  : {OVERSOLD}")
    print(f" Overbought Level: {OVERBOUGHT}")
    print(f" Initial Capital : ₹{initial_capital:,.2f}")
    print(f" Final Value     : ₹{final_value:,.2f}")
    print(f" Strategy Return : {total_return:.2f}%")
    print(f" Buy & Hold      : {buy_hold_return:.2f}%")
    print("=" * 45)


def plot_strategy(df: pd.DataFrame) -> None:
    """Plot price with buy/sell signals and RSI indicator."""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True,
                                         gridspec_kw={"height_ratios": [3, 1.5, 1.5]})

    # Price chart
    ax1.plot(df.index, df["Close"], label="Close Price", color="steelblue", linewidth=1.5)
    buy_signals = df[df["Trade"] > 0]
    sell_signals = df[df["Trade"] < 0]
    ax1.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="lime", s=100, label="Buy", zorder=5)
    ax1.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red", s=100, label="Sell", zorder=5)
    ax1.set_title(f"RSI Strategy — {SYMBOL}", fontsize=14)
    ax1.set_ylabel("Price (INR)")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # RSI chart
    ax2.plot(df.index, df["RSI"], label="RSI", color="darkorange", linewidth=1.2)
    ax2.axhline(OVERBOUGHT, color="red", linestyle="--", linewidth=1, label=f"Overbought ({OVERBOUGHT})")
    ax2.axhline(OVERSOLD, color="green", linestyle="--", linewidth=1, label=f"Oversold ({OVERSOLD})")
    ax2.fill_between(df.index, OVERSOLD, df["RSI"], where=(df["RSI"] < OVERSOLD), alpha=0.2, color="green")
    ax2.fill_between(df.index, OVERBOUGHT, df["RSI"], where=(df["RSI"] > OVERBOUGHT), alpha=0.2, color="red")
    ax2.set_ylabel("RSI")
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(alpha=0.3)

    # Portfolio value
    ax3.plot(df.index, df["Portfolio_Value"], color="purple", linewidth=1.5)
    ax3.set_title("Portfolio Value Over Time")
    ax3.set_ylabel("Value (INR)")
    ax3.set_xlabel("Date")
    ax3.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("rsi_strategy.png", dpi=150)
    plt.show()
    print("Chart saved as rsi_strategy.png")


if __name__ == "__main__":
    data = fetch_data(SYMBOL, START_DATE, END_DATE)
    data = compute_signals(data, RSI_PERIOD, OVERSOLD, OVERBOUGHT)
    data = backtest(data, INITIAL_CAPITAL)
    print_performance(data, INITIAL_CAPITAL)
    plot_strategy(data)

# ─── LIVE TRADING INTEGRATION (Zerodha Kite Connect) ─────────────────────────
# Replace fetch_data() with real-time Kite Connect API calls.
# Visit https://tradevectors.com for live trading setup guides.
# ─────────────────────────────────────────────────────────────────────────────
