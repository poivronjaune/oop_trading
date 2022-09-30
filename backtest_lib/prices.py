import os
import pandas as pd
import yfinance as yf
from datetime import datetime
import common

class Prices():
    DEFAULT_SYMBOL = "AAPL"
    DEFAULT_START_DATE = datetime(2018, 1, 1)
    DEFAULT_END_DATE = datetime.now()
    DEFAULT_INTERVAL = 'D' # 'D' : Daily, 'M' : Minute, 'H': Hour

    def __init__(self, symbol=None):
        if symbol is None:
            self.symbol = Prices.DEFAULT_SYMBOL
        else:
            self.symbol = symbol
        self.start_date = Prices.DEFAULT_START_DATE
        self.end_date = Prices.DEFAULT_END_DATE
        self.interval = Prices.DEFAULT_INTERVAL
        self.data = None

    def __repr__(self) -> str:
        str_items_in_data = "Empty" if self.data is None else f"{len(self.data)} items"
        interval_text = {'D':'Daily', 'H':'Hour', 'M':'Minute'}
        info_to_str = f"\nClass attributes:\n"
        info_to_str += f"class        : {type(self).__name__} <- {self.__class__.__bases__[0].__name__}\n"
        info_to_str += f"symbol       : {self.symbol}\n"
        info_to_str += f"start_date   : {self.start_date}\n"
        info_to_str += f"end_date     : {self.end_date}\n"
        info_to_str += f"interval     : {self.interval} ({interval_text.get(self.interval)})\n"
        info_to_str += f"data         : {str_items_in_data}\n"

        return info_to_str

    def download_prices(self):
        if self.interval and self.interval == 'D':
            self.data = self.download_daily_prices(self.symbol, self.start_date, self.end_date)
        
        if self.interval and self.interval == 'M':
            self.data = self.download_minute_prices(self.symbol)

        self.data.insert(0, "Symbol", self.symbol)
        self.data.index = self.data.index.astype("object")

    def download_daily_prices(self, symbol, start_date, end_date):
        data = yf.download(symbol, start_date, end_date, interval='1d')
        return data

    def download_minute_prices(self, symbol):
        data = yf.download(symbol, period='max', interval='1m')
        if len(data) < 1:
            raise ValueError('No data returned from Yahoo')

        self.start_date = data.index.min().date()
        self.end_date = data.index.max().date()
        return data

    def load_data_from_file(self, file_path, file_name):
        file_to_load = os.path.join(file_path, file_name)
        if not os.path.exists(file_to_load):
            print("No file found!")
            return

        data = pd.read_csv(file_to_load, index_col=False)
        data.index = self.data.index.astype("object")
        
        self.data = data

    def to_csv(self, file_path='.', file_name='prices.csv'):
        file_name = common.create_storage_folder_and_return_full_file_name(file_path, file_name)
        self.data.to_csv(file_name, index=True, sep=',', mode='w')

if __name__ == "__main__":
    prices = Prices()           # Need to set symbol if not using default 'AAPL'
    prices.symbol = 'TSLA'
    prices.interval = 'D'
    prices.download_prices()
    print(prices)
    print(prices.data)
    print(f"Min date: {prices.data.index.min()}")
    print(f"Max date: {prices.data.index.max()}")
    prices.to_csv('tmp','tsla_prices.csv')

    # prices2 = Prices()
    # prices2.load_data_from_file('data','prices-aapl.csv')

