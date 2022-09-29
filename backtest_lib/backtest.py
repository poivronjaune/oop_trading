import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import common
from datetime import datetime, timedelta
from dateutil import parser

from scipy.signal import argrelextrema

# UTILITY FUNCTION
# def _extract_date(date_param):
#     try:
#         date_val = parser.parse(date_param)
#     except Exception:
#         date_val = None

#     if isinstance(date_param, datetime):
#         date_val = date_param

#     return date_val


class Backtest:
    DEFAULT_SYMBOL = "AAPL"
    DEFAULT_START_DATE = datetime(2018, 1, 1)
    DEFAULT_END_DATE = datetime.now()
    DEFAULT_INTERVAL = 'D' # 'D' : Daily, 'M' : Minute, 'H': Hour

    def __init__(self, symbol=None):
        if symbol == None:
            self._symbol = Backtest.DEFAULT_SYMBOL
        else:
            self.symbol = symbol

        self._end_date = Backtest.DEFAULT_END_DATE
        self._start_date = Backtest.DEFAULT_START_DATE
        self.interval = Backtest.DEFAULT_INTERVAL
        self.cash = 1000
        self.data = None

    def __repr__(self) -> str:
        str_items_in_data = "Empty" if self.data is None else f"{len(self.data)} items"

        info_to_str = f"\nClass attributes:\n"
        info_to_str += f"class        : {type(self).__name__} <- {self.__class__.__bases__[0].__name__}\n"
        info_to_str += f"symbol       : {self.symbol}\n"
        info_to_str += f"start date   : {self.start_date}\n"
        info_to_str += f"end date     : {self.end_date}\n"
        info_to_str += f"interval     : {self.interval}\n"
        info_to_str += f"cash         : {self.cash}\n"
        info_to_str += f"data         : {str_items_in_data}\n"

        return info_to_str

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        # Sanity checks to fix bad parameter so we get only the first item if more than 1 symbol passed
        if isinstance(symbol, list):
            symbol = " ".join(symbol)
        symbol = symbol.replace(",", " ")
        symbols = symbol.split(" ")

        if len(symbols[0]) > 0:
            self._symbol = symbols[0]
        else:
            self._symbol = Backtest.DEFAULT_SYMBOL
            raise ValueError("Invalid stock symbol.")

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, date_param):
        #date_val = _extract_date(date_param)
        date_val = common.extract_date(date_param)

        if (date_val is not None) and (date_val < self.end_date):
            self._start_date = date_val
        else:
            raise ValueError("Invalid date or start_date > end_date.")

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, date_param):
        #date_val = _extract_date(date_param)
        date_val = common.extract_date(date_param)

        if (date_val is not None) and (date_val > self.start_date):
            self._end_date = date_val
        else:
            raise ValueError("Invalid date or end_date < start_date.")


#https://raposa.trade/blog/higher-highs-lower-lows-and-calculating-price-trends-in-python/
def plot1(data):
    data['local_max'] = data['Close'][(data['Close'].shift(1) < data['Close']) & (data['Close'].shift(-1) < data['Close'])]
    data['local_min'] = data['Close'][(data['Close'].shift(1) > data['Close']) & (data['Close'].shift(-1) > data['Close'])]

    plt.figure(figsize=(15, 8))
    plt.plot(data['Close'], zorder=0)
    plt.scatter(data.index, prices_df['local_max'], s=100,
      label='Maxima', marker='^', c=colors[1])
    plt.scatter(data.index, prices_df['local_min'], s=100,
      label='Minima', marker='v', c=colors[2])
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.title(f'Local Maxima and Minima for {ticker}')
    plt.legend()
    plt.show()

def plot2(data, order):
    max_idx = argrelextrema(data['Close'].values, np.greater, order=order)[0]
    min_idx = argrelextrema(data['Close'].values, np.less, order=order)[0]
    plt.figure(figsize=(15, 8))
    plt.plot(data['Close'], zorder=0)
    plt.scatter(data.iloc[max_idx].index, data.iloc[max_idx]['Close'],
    label='Maxima', s=100, color=colors[1], marker='^')
    plt.scatter(data.iloc[min_idx].index, data.iloc[min_idx]['Close'],
    label='Minima', s=100, color=colors[2], marker='v')

    plt.legend()
    plt.show()    


if __name__ == '__main__':
    ticker = 'TSLA'
    df = pd.read_csv(os.path.join('tmp','tsla_prices.csv'), index_col=0)
    prices_df = df[-900:].copy()
    prices_df['DayChange'] = prices_df['Close'].pct_change()
    prices_df['Trend'] = np.where(prices_df['DayChange'] > 0, 'Up', 'Down')
    prices_df['TrendUpStart'] = (prices_df['Trend'] == 'Up') & (prices_df['Trend'].shift(1) == 'Down')
    prices_df['TrendDownStart'] = (prices_df['Trend'] == 'Down') & (prices_df['Trend'].shift(1) == 'Up')
    prices_df['TrendStartDate'] = np.where(prices_df['TrendUpStart'] | prices_df['TrendDownStart'], prices_df.index, 0)
    prices_df['TrendStartDate'] = prices_df['TrendStartDate'].replace(0, method='ffill')
    prices_df['TrendSequence'] = prices_df.groupby('TrendStartDate').cumcount() + 1
    

    print(prices_df.tail(20))

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    #plot1(prices_df)
    plot2(prices_df, 5)

