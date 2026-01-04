import pandas as pd
import numpy as np
import math
import sys
import time
import datetime

# PRIME HARMONICS
EULER_CYCLE = 263  # The Expansion Wave (Days)
GRAVITY_CYCLE = 97 # The Correction Wave (Days)
PHI_INV_SQ = 0.382 # The Golden Floor
EPSILON_DELTA = 0.724 # The Harmonic Correction Constant (RI1 PHA)

class EulerBot:
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0 # 0 = Cash, 1 = Long
        self.entry_price = 0
        self.trades = []
        
    def load_data(self, ticker):
        """
        Fetches live data from Yahoo Finance.
        """
        print(f"Fetching live data for {ticker}...")
        
        # Calculate timestamps
        end_time = int(time.time())
        start_time = end_time - (5 * 365 * 24 * 60 * 60) # 5 Years ago
        
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_time}&period2={end_time}&interval=1d&events=history"
        
        try:
            df = pd.read_csv(url)
            df['date'] = pd.to_datetime(df['Date'])
            df = df.rename(columns={'Close': 'close', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Volume': 'volume'})
            df = df.sort_values('date').reset_index(drop=True)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            # Fallback to local file if network fails
            print("Falling back to local CSV...")
            filename = "btc_data.csv" if "BTC" in ticker else "spx_data.csv"
            df = pd.read_csv(f"/home/ubuntu/HARMONIA-DSL/{filename}")
            df['date'] = pd.to_datetime(df['timestamp'], unit='s')
            df = df.sort_values('date').reset_index(drop=True)
            return df
        
    def calculate_signals(self, df):
        """
        Generates signals based on the 263/97 Harmonic and Epsilon Correction.
        """
        # We need at least 263 days of data to start
        df['signal'] = 0 # 0=Hold, 1=Buy, -1=Sell
        
        # Calculate Rolling Highs/Lows for the Prime Cycles
        df['min_97'] = df['close'].rolling(window=GRAVITY_CYCLE).min()
        df['max_97'] = df['close'].rolling(window=GRAVITY_CYCLE).max()
        
        df['min_263'] = df['close'].rolling(window=EULER_CYCLE).min()
        df['max_263'] = df['close'].rolling(window=EULER_CYCLE).max()
        
        # THE STRATEGY (TREND FOLLOWING + HARMONIC CORRECTION)
        # BUY when:
        # Price CROSSES ABOVE the 97-Day Moving Average (Gravity Lift)
        
        # SELL when:
        # Price CROSSES BELOW the 97-Day Moving Average (Gravity Drop)
        
        df['ma_97'] = df['close'].rolling(window=GRAVITY_CYCLE).mean()
        df['ma_263'] = df['close'].rolling(window=EULER_CYCLE).mean()
        
        # Harmonic Ratio: Growth / Gravity
        df['harmonic_ratio'] = df['ma_263'] / df['ma_97']
        
        # Epsilon Correction Band
        # We use 0.724 as a volatility buffer factor
        df['volatility'] = df['close'].rolling(window=GRAVITY_CYCLE).std()
        df['epsilon_band'] = df['volatility'] * EPSILON_DELTA
        
        for i in range(EULER_CYCLE, len(df)):
            price = df.loc[i, 'close']
            ma_97 = df.loc[i, 'ma_97']
            epsilon = df.loc[i, 'epsilon_band']
            
            prev_price = df.loc[i-1, 'close']
            prev_ma_97 = df.loc[i-1, 'ma_97']
            prev_epsilon = df.loc[i-1, 'epsilon_band']
            
            # Logic: Crossover with Epsilon Buffer
            # Buy only if price breaks MA_97 + Epsilon (Confirmation)
            if prev_price < (prev_ma_97 + prev_epsilon) and price > (ma_97 + epsilon):
                df.loc[i, 'signal'] = 1 # BUY (Breakout)
            
            # Sell only if price breaks MA_97 - Epsilon (Confirmation)
            elif prev_price > (prev_ma_97 - prev_epsilon) and price < (ma_97 - epsilon):
                df.loc[i, 'signal'] = -1 # SELL (Breakdown)
                
        return df
        
    def backtest(self, df):
        print(f"Starting Backtest with ${self.initial_capital:,.2f}")
        
        for i in range(len(df)):
            signal = df.loc[i, 'signal']
            price = df.loc[i, 'close']
            date = df.loc[i, 'date'].date()
            
            if signal == 1 and self.position == 0:
                # BUY
                self.position = self.capital / price
                self.capital = 0
                self.entry_price = price
                self.trades.append({'type': 'BUY', 'date': date, 'price': price})
                # print(f"[{date}] BUY  @ ${price:,.2f}")
                
            elif signal == -1 and self.position > 0:
                # SELL
                self.capital = self.position * price
                profit = (price - self.entry_price) / self.entry_price
                self.position = 0
                self.trades.append({'type': 'SELL', 'date': date, 'price': price, 'profit': profit})
                # print(f"[{date}] SELL @ ${price:,.2f} | PnL: {profit*100:.2f}%")
                
        # Final Value
        final_value = self.capital
        if self.position > 0:
            final_value = self.position * df.iloc[-1]['close']
            
        return final_value
        
    def get_current_status(self, df):
        last_row = df.iloc[-1]
        price = last_row['close']
        
        print("\n=== EULER BOT V2 (PHA ENHANCED) STATUS REPORT ===")
        print(f"Date: {last_row['date'].date()}")
        print(f"Price: ${price:,.2f}")
        print(f"97-Day Range: ${last_row['min_97']:,.2f} - ${last_row['max_97']:,.2f}")
        print(f"263-Day Range: ${last_row['min_263']:,.2f} - ${last_row['max_263']:,.2f}")
        
        # Check Signals
        ma_97 = last_row['ma_97']
        epsilon = last_row['epsilon_band']
        upper_band = ma_97 + epsilon
        lower_band = ma_97 - epsilon
        
        print(f"97-Day MA: ${ma_97:,.2f}")
        print(f"Epsilon Band (±{EPSILON_DELTA}σ): ${epsilon:,.2f}")
        print(f"Buy Threshold: ${upper_band:,.2f}")
        print(f"Sell Threshold: ${lower_band:,.2f}")
        
        print("\n--- HARMONIC ANALYSIS ---")
        if price > upper_band:
            print("[YES] Price is ABOVE Gravity Wave + Epsilon (Strong Bullish)")
        elif price < lower_band:
            print("[NO]  Price is BELOW Gravity Wave - Epsilon (Strong Bearish)")
        else:
            print("[~]   Price is INSIDE the Epsilon Buffer (Neutral/Choppy)")
            
        print("\n--- RECOMMENDATION ---")
        if price > upper_band:
            print(">>> SIGNAL: HOLD LONG (Ride the Wave) <<<")
        elif price < lower_band:
            print(">>> SIGNAL: STAY CASH (Wait for Breakout) <<<")
        else:
            print(">>> SIGNAL: HOLD CURRENT POSITION (Noise Filter Active) <<<")

if __name__ == "__main__":
    bot = EulerBot()
    
    # Analyze BTC
    print("\n--------------------------------")
    print("RUNNING EULER BOT V2 ON BITCOIN (BTC-USD)")
    print("--------------------------------")
    df_btc = bot.load_data('BTC-USD')
    df_btc = bot.calculate_signals(df_btc)
    final_btc = bot.backtest(df_btc)
    
    buy_hold_btc = (10000 / df_btc.iloc[0]['close']) * df_btc.iloc[-1]['close']
    print(f"\nFinal Portfolio Value: ${final_btc:,.2f}")
    print(f"Buy & Hold Value:      ${buy_hold_btc:,.2f}")
    print(f"Performance vs B&H:    {(final_btc/buy_hold_btc - 1)*100:.2f}%")
    
    bot.get_current_status(df_btc)
    
    # Analyze SPX
    print("\n--------------------------------")
    print("RUNNING EULER BOT V2 ON S&P 500 (^GSPC)")
    print("--------------------------------")
    bot_spx = EulerBot()
    df_spx = bot_spx.load_data('^GSPC')
    df_spx = bot_spx.calculate_signals(df_spx)
    final_spx = bot_spx.backtest(df_spx)
    
    buy_hold_spx = (10000 / df_spx.iloc[0]['close']) * df_spx.iloc[-1]['close']
    print(f"\nFinal Portfolio Value: ${final_spx:,.2f}")
    print(f"Buy & Hold Value:      ${buy_hold_spx:,.2f}")
    print(f"Performance vs B&H:    {(final_spx/buy_hold_spx - 1)*100:.2f}%")
    
    bot_spx.get_current_status(df_spx)
