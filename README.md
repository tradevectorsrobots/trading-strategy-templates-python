# Python Trading Strategy Templates for NSE/BSE India

**Gateway to Automated Trading & Algorithmic Trading Software for Indian & Global Markets**

> **Ready-to-use Python algorithmic trading strategy templates** for Indian and global financial markets.
> Maintained by [**Trade Vectors LLP**](https://tradevectors.com) — India's algorithmic trading software development company.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Trade Vectors](https://img.shields.io/badge/By-Trade%20Vectors%20LLP-purple)](https://tradevectors.com)

---

## About Trade Vectors LLP

[Trade Vectors LLP](https://tradevectors.com) is a specialized **algorithmic trading software development company** based in India (Mumbai / Surat) and Canada with 13+ years of experience in:

- **Custom Algorithmic Trading Software Development** — Institutional-grade automated systems for equities, futures, options, commodities, forex, and digital assets
- **Broker API Integration Services** — Secure REST and WebSocket API integration with Interactive Brokers, MetaTrader, Angel One, Zerodha, Kotak, IC Markets, and more
- **Trading Backtesting Software Development** — Advanced historical simulation and strategy validation engines with Sharpe ratio, drawdown, and equity curve analytics
- **Automated Trading Consulting** — Technology consultancy for migrating manual workflows into rules-based, software-driven systems
- **AI & Machine Learning for Trading** — Neural networks, regression models, deep learning, NLP-based news sentiment integration

> **Contact:** [contact@tradevectors.com](mailto:contact@tradevectors.com) | [Book a Free Consultation](https://tradevectors.com/book-appointment.php)

---

## Strategy Templates Included

| # | Strategy | File | Indicators | Asset Classes |
|---|----------|------|------------|---------------|
| 1 | Moving Average Crossover | `moving_average_crossover.py` | SMA 20, SMA 50 (Golden/Death Cross) | Equities, Futures, Forex |
| 2 | RSI Mean Reversion | `rsi_strategy.py` | RSI 14 (Oversold/Overbought) | Equities, Commodities, Crypto |
| 3 | MACD Momentum | `macd_strategy.py` | MACD 12/26/9, Signal Line, Histogram | Equities, Forex, Index Futures |
| 4 | Bollinger Bands Mean Reversion | `bollinger_bands_strategy.py` | BB 20,2 with %B and Bandwidth | Equities, Options Premium, Forex |

### Coming Soon
- `supertrend_strategy.py` — ATR-based Supertrend for NSE/BSE trending markets
- `options_pcr_strategy.py` — Put-Call Ratio analytics for NIFTY/BANKNIFTY
- `multi_indicator_signal_generator.py` — Supertrend + Awesome Oscillator + Stochastic combo
- `pair_trading_strategy.py` — Statistical arbitrage / pairs trading with correlation analysis
- `vwap_strategy.py` — Volume Weighted Average Price intraday strategy
- `risk_management_module.py` — Position sizing, stop-loss automation, portfolio rebalancing

---

## Supported Trading Platforms & Broker APIs

Trade Vectors builds custom trading systems for these platforms. These templates can be adapted to connect with any of the following:

### Indian Brokers & Platforms
| Broker/Platform | API Type | Asset Classes |
|-----------------|----------|---------------|
| **Zerodha Kite Connect** | REST + WebSocket | Equities, F&O, Commodities |
| **Angel One (AngelBroking)** | REST + WebSocket | Equities, F&O, Commodities |
| **Upstox** | REST + WebSocket | Equities, F&O |
| **Kotak Securities** | REST | Equities, F&O |
| **NEST / ODIN / Symphony** | FIX Protocol | Multi-asset |
| **Tradetron** | REST | Strategy automation |

### Global Brokers & Platforms
| Broker/Platform | API Type | Asset Classes |
|-----------------|----------|---------------|
| **Interactive Brokers (IBKR)** | REST + WebSocket + FIX | Equities, Forex, Futures, Options |
| **MetaTrader 5 (MT5)** | MQL5 + Python bridge | Forex, CFDs, Futures |
| **TradingView** | Pine Script + Webhooks | Multi-asset charting |
| **NinjaTrader** | C# + REST | Futures, Forex |
| **TradeStation** | EasyLanguage + REST | Equities, Futures |
| **QuantConnect** | Python LEAN | Multi-asset backtesting |
| **Quantower** | C# .NET | Futures, Forex |
| **AmiBroker** | AFL + DLL | Equities, Futures |
| **MultiCharts** | PowerLanguage | Multi-asset |
| **IC Markets** | REST | Forex, CFDs |

### Data Feed Providers

| Provider | API Type | Data Coverage |
|----------|----------|---------------|
| **Nanex** | REST + WebSocket | Real-time market data, Level 2 |
| **IQFeed (DTN)** | TCP/IP Socket | Equities, Futures, Forex, Options |
| **CQG** | REST + FIX | Multi-asset global market data |

---

## Types of Trading Strategies Supported

Based on Trade Vectors' expertise, these templates cover and can be extended for:

### Technical Analysis Automation
- Moving Averages (SMA, EMA, WMA), RSI, MACD, Bollinger Bands
- Pattern recognition: Head & Shoulders, Double Top/Bottom, Wedges, Flags, Pennants, Triangles
- Candlestick patterns: Engulfing, Hammer, Shooting Star, Doji, Morning/Evening Star
- Support & Resistance, Trendline breakouts, Channel trading

### Momentum & Trend Following
- Multi-timeframe trend analysis (5-min, 15-min, daily)
- Supertrend, Awesome Oscillator, Stochastic
- Momentum indicator integration

### Mean Reversion & Swing Trading
- Statistical reversal identification
- Bollinger Band mean reversion
- RSI oversold/overbought swing setups

### Quantitative & Statistical Arbitrage
- Pair trading with correlation analysis
- Statistical arbitrage models
- Mathematical trading models

### Options & Derivatives Strategies
- Greeks calculation (Delta, Gamma, Theta, Vega)
- Put-Call Ratio (PCR) analytics for NIFTY / BANKNIFTY
- Spread strategies and volatility-based automation
- ATM strike analytics and open interest tracking

### Multi-Indicator Signal Generation
- Supertrend + Awesome Oscillator + Stochastic combination
- Volume Profile quantitative analysis
- Multi-timeframe confirmation systems

### Commodity & Forex Systems
- Gold, Silver, Crude Oil, Natural Gas
- Currency pair trading (USDINR, EURUSD, GBPUSD, etc.)
- MCX commodity automation

### Cryptocurrency Trading
- 24/7 automated systems for Bitcoin, Ethereum, altcoins
- Level-based entry strategies for crypto exchange APIs
- Round-the-clock monitoring architecture

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/tradevectorsrobots/trading-strategy-templates-python.git
cd trading-strategy-templates-python
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run a Strategy (Example: MACD on RELIANCE.NS)
```bash
python macd_strategy.py
```
Or open any `.py` file, change the `SYMBOL` and date parameters at the top, and run.

### 4. NSE Symbol Format
```python
SYMBOL = "RELIANCE.NS"    # NSE (National Stock Exchange)
SYMBOL = "RELIANCE.BO"   # BSE (Bombay Stock Exchange)
SYMBOL = "NIFTY50.NS"    # NIFTY 50 Index
SYMBOL = "BANKNIFTY.NS"  # Bank Nifty Index
SYMBOL = "GOLDPETAL.MCX" # MCX Gold (via data provider)
```

---

## Technology Stack

These templates are built with:

| Library | Purpose |
|---------|---------|
| `yfinance` | Historical OHLCV data for NSE/BSE/Global markets |
| `pandas` | Data manipulation and time-series analysis |
| `numpy` | Numerical computation and indicator calculation |
| `matplotlib` | Strategy visualization and chart output |

### For Live Trading (Zerodha Kite Connect)
```python
from kiteconnect import KiteConnect
kite = KiteConnect(api_key="YOUR_API_KEY")
kite.set_access_token("YOUR_ACCESS_TOKEN")
# Replace yfinance fetch_data() with kite.historical_data()
```

### For Live Trading (Interactive Brokers)
```python
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# See Trade Vectors IB integration guides at https://tradevectors.com
```

---

## Our Projects (Built by Trade Vectors LLP)

These templates are inspired by real-world projects delivered by Trade Vectors:

| Project | Description | Tech Stack |
|---------|-------------|------------|
| Automated Trading Platform | Multi-broker API integration (IB, Angel, Kotak, IC Markets) with real-time order routing | Python, Node.js, React, Flutter |
| Strategy Configuration Module | Client-defined parameter interface for CASH/FUTURES/OPTIONS segments | C# .NET, SQL Server |
| Multi-Account Trade Execution System | Centralized portfolio management across multiple broker accounts | C# .NET, SQL Server, Serilog |
| Pattern Recognition Trading System | Real-time chart pattern detection with automated execution | C# .NET, Custom algorithms |
| Real-Time Options Analytics Platform | Live PCR analytics, ATM strike metrics for NIFTY/BANKNIFTY | WebSocket, Interactive charts |
| Multi-Indicator Signal Generator | Supertrend + Awesome Oscillator + Stochastic signal engine | Python, Broker APIs |
| 24/7 Cryptocurrency Trading System | Round-the-clock level-based crypto execution | Cloud-based, Exchange APIs |
| Multi-Broker Options Trading Platform | Options strategy automation across Indian brokers simultaneously | Multi-broker REST APIs |
| High-Performance Options Trading System | 300 instruments, 30 orders/sec throttling, 5 portfolios | C# .NET, SQL Server |
| Stock Scanner (4000+ symbols) | High-throughput NSE/BSE/US market scanner with configurable alerts | Nanex data feed, WebSocket |
| IB Options Alert System | Greeks calculation and options scanning via Interactive Brokers API | Python, IBKR API |

---

## Performance Metrics Generated

Every strategy template outputs:
- Total Return vs Buy-and-Hold benchmark
- Sharpe Ratio (in advanced templates)
- Maximum Drawdown
- Win Rate and Win/Loss distribution
- Trade-by-trade execution log
- Portfolio equity curve chart (PNG export)
- Buy/Sell signal dates table

---

## Disclaimer

> Trade Vectors LLP provides **technology development and API integration services only**.
> These templates are for **educational and informational purposes**.
> We do **not** offer investment advice, portfolio management, or fund management services.
> All strategy design, risk management, and execution decisions remain solely with the user.
> Past performance does not guarantee future results.
> Trading involves substantial risk and may not be suitable for all investors.

---

## About the Author

**Kashyap Thakkar** — Co-Founder & Lead Consultant, Trade Vectors LLP

- 13+ years experience in algorithmic trading software development
- **Languages:** Python, Java, C#, C++, SQL
- **Platforms:** Interactive Brokers, MetaTrader 5, QuantConnect, TradingView, NinjaTrader, Zerodha, AngelOne, ThinkOrSwim, NEST, ODIN, Symphony, Quantower
- **Expertise:** HFT systems, multi-broker API integration, options trading automation, AI/ML for trading, Azure cloud infrastructure
- Recognized on **Interactive Brokers' Marketplace** for software development services
- **B.E. Information Technology**, University of Mumbai

---

## Connect & Hire Us

Need custom algorithmic trading software built?

| Channel | Link |
|---------|------|
| Website | [tradevectors.com](https://tradevectors.com) |
| Services | [Algorithmic Trading Software Development](https://tradevectors.com/algorithmic-trading-software-development.php) |
| Broker API | [Broker API Integration Services](https://tradevectors.com/broker-api-integration-services.php) |
| Backtesting | [Backtesting Software Development](https://tradevectors.com/trading-backtesting-software-development.php) |
| AI/ML | [AI & Machine Learning for Trading](https://tradevectors.com/artificial-intelligence-and-machine-learning.php) |
| Projects | [Our Projects Portfolio](https://tradevectors.com/algo-trading-projects.php) |
| Strategies | [Types of Trading Strategies](https://tradevectors.com/algo-trading-strategies.php) |
| Book Call | [Free Consultation](https://tradevectors.com/book-appointment.php) |
| Email | [contact@tradevectors.com](mailto:contact@tradevectors.com) |
| LinkedIn | [linkedin.com/company/tradevectors](https://www.linkedin.com/company/tradevectors) |
| YouTube | [Trade Vectors YouTube Channel](https://www.youtube.com/channel/UCUaaXGA6CQk1QwcZUHkFLLA/videos) |
| Interactive Brokers | [IB Marketplace - Trade Vectors](https://gdcdyn.interactivebrokers.com/Marketplace/InvestorsMarketplace) |

---

*Copyright 2026 Trade Vectors LLP | GSTIN: 27AAJFT1084A1ZE | India & Canada*
