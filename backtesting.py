import os
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt

class Backtest:
    def __init__(self, symbol=None):
        self.symbol = symbol
        if symbol is None:
            self.symbol = 'AAPL'
        
        self.df = yf.download(self.symbol, start='2019-01-01')
        if self.df.empty:
            raise ValueError(f"No data pulled for symbol {symbol}")

        self.calc_indicators()
        self.generate_signals()
        self.run_trades()
        self.profit = self.calc_profit()
        self.max_drawdown = self.profit.min()
        self.cumulative_profit = (self.profit + 1).prod() - 1

    def calc_indicators(self):
        self.df['ma_20']    = self.df.Close.rolling(20).mean()
        self.df['vol']      = self.df.Close.rolling(20).std()
        self.df['upper_bb'] = self.df.ma_20 + (2 * self.df.vol)
        self.df['lower_bb'] = self.df.ma_20 - (2 * self.df.vol)
        self.df['rsi']      = ta.momentum.rsi(self.df.Close, window=6)
        self.df.dropna(inplace=True)

    def generate_signals(self):
        # [buy signals, sell signals]
        conditions = [
            (self.df.rsi < 30) & (self.df.Close < self.df.lower_bb),
            (self.df.rsi > 70) & (self.df.Close > self.df.upper_bb)
        ]
        choices = ['Buy', 'Sell']
        self.df['signal'] = np.select(conditions, choices)
        self.df.signal = self.df.signal.shift()
        self.df.dropna(inplace=True)

    def run_trades(self):
        position = False
        buydates, selldates = [], []

        for index, row in self.df.iterrows():
            # Don't forget we shifted our signals so buy is on our real buy date (next day's open)
            if not position and row['signal'] == 'Buy':
                position = True
                buydates.append(index)
            
            # Don't forget we shifted our signals so sell is on our real sell date (next day's open)
            if position and row['signal'] == 'Sell':
                position = False
                selldates.append(index)

        self.buy_arr  = self.df.loc[buydates].Open    # Use buydates index (date) to get the open price of the buy trade
        self.sell_arr = self.df.loc[selldates].Open   # Use buydates index (date) to get the open price of the buy trade


    def calc_profit(self):
        # Calculate profits only for closed trades and filter out the open trades
        # if open position, then the last buy_signal is greater the the last sell_signal (buy_arr length is greater than sell_arr length)
        if self.buy_arr.index[-1] > self.sell_arr.index[-1]:
            self.buy_arr = self.buy_arr[:-1]
        
        return (self.sell_arr.values - self.buy_arr.values) / self.buy_arr.values

    def plot_chart(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.df.Close)
        plt.scatter(self.buy_arr.index, self.buy_arr.values, marker='^', c='g')
        plt.scatter(self.sell_arr.index, self.sell_arr.values, marker='v', c='r')

        #plt.show()

    def log_trades(self, file_name=None):
        path_str = 'LOG\\'
        if file_name is None:
            file_name = 'trades.csv'
        
        trades_df = pd.DataFrame(data=self.buy_arr)
        trades_df = trades_df.reset_index()
        trades_df.index.rename('trade_id', inplace=True)
        trades_df.rename(columns={'Date': 'buy_date', 'Open': 'buy_price'}, inplace=True)
        trades_df['sell_date']  = self.sell_arr.index
        trades_df['sell_price'] = self.sell_arr.values
        trades_df['profit_ratio'] = self.profit
        trades_df['profit_value'] = trades_df['sell_price'] - trades_df['buy_price']

        trades_df.to_csv(f"{os.path.join(path_str,file_name)}", index=False)
        
            
