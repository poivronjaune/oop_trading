from datetime import datetime, timedelta
from dateutil import parser
import yfinance as yf


class Backtest:
    DEFAULT_SYMBOL = "AAPL"

    def __init__(self, symbol=None):
        if symbol == None:
            self._symbol = Backtest.DEFAULT_SYMBOL
        else:
            self.symbol = symbol

        # self.start_date = datetime(2018, 1, 1)
        self.start_date = "2018-1-1"
        self.end_date = datetime.now()
        self.data = None

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
        date_val = None
        if isinstance(date_param, str):
            # date_val = datetime(datetime.strptime('Jun 1 2005  1:33PM', '%Y/%m/%d %I:%M'))
            date_val = parser.parse(date_param)
            
        
        if date_val is not None:
            self._start_date = date_val
        else:
            raise ValueError('Invalid date.')

    def download_prices(self):
        data = yf.download(self.symbol, self.start_date, self.end_date)
        self.data = data
