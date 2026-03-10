"""
0DTE SPXW Options Writing Strategy (Automated via IBKR API)
Trade Vectors | https://tradevectors.com

Strategy Logic:
- Target: SPXW (S&P 500 Weekly Options) 0DTE (Zero Days to Expiration)
- Entry: Credit Spread (Bull Put or Bear Call) or Iron Condor based on premium thresholds
- Automation: Interactive Brokers (IBKR) API (ib_insync)
"""

import logging
from ib_insync import *
import datetime

# --- CONFIGURATION ---
IB_HOST = '127.0.0.1'
IB_PORT = 7497  # Use 7496 for Live, 7497 for Paper Trading
CLIENT_ID = 10

SYMBOL = "SPX"
STRIKE_DISTANCE = 5  # Distance between spread legs
DELTA_TARGET = 0.10  # Target delta for short leg
QUANTITY = 1

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SPX0DTEStrategy:
    def __init__(self):
        self.ib = IB()

    def connect(self):
        try:
            self.ib.connect(IB_HOST, IB_PORT, clientId=CLIENT_ID)
            logging.info("Connected to IBKR API")
        except Exception as e:
            logging.error(f"Connection failed: {e}")

    def get_spxw_contract(self):
        """Fetch SPX weekly options for the current expiration."""
        spx = Index('SPX', 'CBOE')
        self.ib.qualifyContracts(spx)
        
        # Get option chains
        chains = self.ib.reqSecDefOptParams(spx.symbol, '', spx.secType, spx.conId)
        chain = next(c for c in chains if c.exchange == 'SMART')
        
        # Get 0DTE expiration (today)
        today = datetime.datetime.now().strftime('%Y%m%d')
        expirations = sorted([e for e in chain.expirations if e == today])
        
        if not expirations:
            logging.warning("No 0DTE expirations found for today.")
            return None
        
        return chain

    def place_spread_order(self, action, strike, right):
        """Place a credit spread order."""
        # This is a simplified template for demonstration
        logging.info(f"Preparing {action} {right} spread at strike {strike}")
        # In a real system, you would define the legs and use a Bag contract
        pass

    def run(self):
        self.connect()
        chain = self.get_spxw_contract()
        if chain:
            logging.info(f"Fetched option chain for {SYMBOL}")
            # Logic for selecting strikes and placing orders goes here
        
        self.ib.disconnect()

if __name__ == "__main__":
    strategy = SPX0DTEStrategy()
    strategy.run()
