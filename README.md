# Python Trading Strategy Templates for NSE/BSE India

**Gateway to Automated Trading & Algorithmic Trading Software for Indian & Global Markets**

> **Ready-to-use Python algorithmic trading strategy templates** for Indian and global financial markets. Maintained by [**Trade Vectors LLP**](https://tradevectors.com/) — India's algorithmic trading software development company.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Trade Vectors](https://img.shields.io/badge/By-Trade%20Vectors%20LLP-purple)](https://tradevectors.com)

---

## About Trade Vectors LLP

[Trade Vectors LLP](https://tradevectors.com/) is a specialized **algorithmic trading software development company** based in India (Mumbai / Surat) and Canada with 13+ years of experience in:

* • **Custom Algorithmic Trading Software Development** — Institutional-grade automated systems for equities, futures, options, commodities, forex, and digital assets
* • **Broker API Integration Services** — Secure REST and WebSocket API integration with Interactive Brokers, MetaTrader, Angel One, Zerodha, Kotak, IC Markets, and more
* • **Trading Backtesting Software Development** — Advanced historical simulation and strategy validation engines with Sharpe ratio, drawdown, and equity curve analytics
* • **Automated Trading Consulting** — Technology consultancy for migrating manual workflows into rules-based, software-driven systems
* • **AI & Machine Learning for Trading** — Neural networks, regression models, deep learning, NLP-based news sentiment integration

> **Contact:** [contact@tradevectors.com](mailto:contact@tradevectors.com) | [Book a Free Consultation](https://tradevectors.com/book-appointment.php)

---

## Strategy Templates Included

| # | Strategy | File | Indicators | Asset Classes |
|---|---|---|---|---|
| 1 | Moving Average Crossover | `moving_average_crossover.py` | SMA 20, SMA 50 (Golden/Death Cross) | Equities, Futures, Forex |
| 2 | RSI Mean Reversion | `rsi_strategy.py` | RSI 14 (Oversold/Overbought) | Equities, Commodities, Crypto |
| 3 | MACD Momentum | `macd_strategy.py` | MACD 12/26/9, Signal Line, Histogram | Equities, Forex, Index Futures |
| 4 | Bollinger Bands Mean Reversion | `bollinger_bands_strategy.py` | BB 20,2 with %B and Bandwidth | Equities, Options Premium, Forex |
| 5 | Pairs Trading (Statistical Arbitrage) | `pairs_trading_strategy.py` | Correlation, Cointegration, Z-Score | Equities, NSE/BSE |
| 6 | 0DTE SPXW Options Writing | `0dte_spxw_options_writing_strategy.py` | Delta, Theta, Premium Thresholds | SPX Index Options (IBKR API) |

### Coming Soon
- `supertrend_strategy.py` — ATR-based Supertrend for NSE/BSE trending markets
- `options_pcr_strategy.py` — Put-Call Ratio analytics for NIFTY/BANKNIFTY
- `vwap_strategy.py` — Volume Weighted Average Price intraday strategy
- `risk_management_module.py` — Position sizing, stop-loss automation, portfolio rebalancing

---

## Supported Trading Platforms & Broker APIs

Trade Vectors builds custom trading systems for these platforms. These templates can be adapted to connect with any of the following:

### Indian Brokers & Platforms
| Broker/Platform | API Type | Asset Classes |
|---|---|---|
| **Zerodha Kite Connect** | REST + WebSocket | Equities, F&O, Commodities |
| **Angel One (AngelBroking)** | REST + WebSocket | Equities, F&O, Commodities |
| **Upstox** | REST + WebSocket | Equities, F&O |
| **Kotak Securities** | REST | Equities, F&O |
| **NEST / ODIN / Symphony** | FIX Protocol | Multi-asset |
| **Tradetron** | REST | Strategy automation |

### Global Brokers & Platforms
| Broker/Platform | API Type | Asset Classes |
|---|---|---|
| **Interactive Brokers (IBKR)** | REST + WebSocket + FIX | Equities, Forex, Futures, Options |
| **MetaTrader 5 (MT5)** | MQL5 + Python bridge | Forex, CFDs, Futures |
| **TradingView** | Pine Script + Webhooks | Multi-asset charting |
| **NinjaTrader** | C# + REST | Futures, Forex |

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

### 3. Run a Strategy (Example: 0DTE SPXW on IBKR)
```bash
python 0dte_spxw_options_writing_strategy.py
```

---

## Disclaimer

> Trade Vectors LLP provides **technology development and API integration services only**. These templates are for **educational and informational purposes**. We do **not** offer investment advice, portfolio management, or fund management services. All strategy design, risk management, and execution decisions remain solely with the user. Past performance does not guarantee future results. Trading involves substantial risk and may not be suitable for all investors.

Copyright 2026 Trade Vectors LLP | GSTIN: 27AAJFT1084A1ZE | India & Canada
