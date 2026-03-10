import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.api import OLS
import warnings
warnings.filterwarnings('ignore')

class PairsTradingStrategy:
    def __init__(self, filepath, corr_threshold=0.7, pvalue_threshold=0.05):
        self.filepath = filepath
        self.corr_threshold = corr_threshold
        self.pvalue_threshold = pvalue_threshold
        self.df = None
        self.pairs_df = None

    def load_data(self):
        """Load stock price data from CSV file."""
        self.df = pd.read_csv(self.filepath, index_col=0, parse_dates=True)
        print(f"Loaded data shape: {self.df.shape}")
        return self.df

    def test_cointegration(self):
        """Test cointegration for highly correlated pairs."""
        stocks = self.df.columns
        n = len(stocks)
        pairs = []

        print("
COINTEGRATION TESTING")
        for i in range(n):
            for j in range(i + 1, n):
                stock1, stock2 = stocks[i], stocks[j]
                corr = self.df[stock1].corr(self.df[stock2])
                
                if abs(corr) < self.corr_threshold:
                    continue

                try:
                    score, pvalue, _ = coint(self.df[stock1], self.df[stock2])
                    if pvalue < self.pvalue_threshold:
                        model = OLS(self.df[stock1], self.df[stock2]).fit()
                        hedge_ratio = model.params[0]
                        spread = self.df[stock1] - hedge_ratio * self.df[stock2]
                        adf_stat, adf_pval, _, _, _, _ = adfuller(spread)

                        pairs.append({
                            'stock1': stock1, 'stock2': stock2,
                            'correlation': corr, 'coint_pvalue': pvalue,
                            'hedge_ratio': hedge_ratio, 'spread_mean': spread.mean(),
                            'spread_std': spread.std(), 'adf_pvalue': adf_pval
                        })
                except:
                    continue

        self.pairs_df = pd.DataFrame(pairs)
        print(f"Found {len(self.pairs_df)} cointegrated pairs.")
        return self.pairs_df

class PairsTradingBacktest:
    def __init__(self, df, pair_info, entry_std=1.5, exit_std=0.3, stop_loss_std=4.0):
        self.df = df
        self.stock1 = pair_info['stock1']
        self.stock2 = pair_info['stock2']
        self.hedge_ratio = pair_info['hedge_ratio']
        self.spread_mean = pair_info['spread_mean']
        self.spread_std = pair_info['spread_std']
        self.entry_std = entry_std
        self.exit_std = exit_std
        self.stop_loss_std = stop_loss_std
        self.trades = []
        self.position = None

    def run(self, initial_capital=100000):
        spread = self.df[self.stock1] - self.hedge_ratio * self.df[self.stock2]
        zscore = (spread - self.spread_mean) / self.spread_std
        capital = initial_capital

        for i in range(1, len(self.df)):
            date = self.df.index[i]
            z = zscore.iloc[i]
            p1, p2 = self.df[self.stock1].iloc[i], self.df[self.stock2].iloc[i]

            if self.position is None:
                if z > self.entry_std: # Short spread
                    self.position = {'type': 'shortspread', 'date': date, 'p1': p1, 'p2': p2, 'cap': capital * 0.5}
                elif z < -self.entry_std: # Long spread
                    self.position = {'type': 'longspread', 'date': date, 'p1': p1, 'p2': p2, 'cap': capital * 0.5}
            else:
                exit = False
                if (self.position['type'] == 'shortspread' and z < self.exit_std) or \
                   (self.position['type'] == 'longspread' and z > -self.exit_std) or \
                   abs(z) > self.stop_loss_std:
                    exit = True
                
                if exit:
                    pnl = self.calculate_pnl(p1, p2)
                    capital += pnl
                    self.trades.append({'date': date, 'pnl': pnl, 'return': (pnl/(self.position['cap']*2))*100})
                    self.position = None
        return capital

    def calculate_pnl(self, p1, p2):
        if self.position['type'] == 'shortspread':
            return self.position['cap'] * (self.position['p1'] - p1)/self.position['p1'] + \
                   self.position['cap'] * (p2 - self.position['p2'])/self.position['p2']
        else:
            return self.position['cap'] * (p1 - self.position['p1'])/self.position['p1'] + \
                   self.position['cap'] * (self.position['p2'] - p2)/self.position['p2']

if __name__ == "__main__":
    strategy = PairsTradingStrategy('stock_data.csv')
    df = strategy.load_data()
    pairs = strategy.test_cointegration()
    
    for _, pair in pairs.iterrows():
        backtester = PairsTradingBacktest(df, pair)
        final = backtester.run()
        print(f"Pair {pair['stock1']}-{pair['stock2']} Final Capital: {final:.2f}")
