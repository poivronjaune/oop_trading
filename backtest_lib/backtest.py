from datetime import datetime, timedelta
from dateutil import parser
import yfinance as yf


# UTILITY FUNCTION
def _extract_date(date_param):
    try:
        date_val = parser.parse(date_param)
    except Exception:
        date_val = None

    if isinstance(date_param, datetime):
        date_val = date_param

    return date_val


class Backtest:
    DEFAULT_SYMBOL = "AAPL"
    DEFAULT_START_DATE = datetime(2018, 1, 1)
    DEFAULT_END_DATE = datetime.now()

    def __init__(self, symbol=None):
        if symbol == None:
            self._symbol = Backtest.DEFAULT_SYMBOL
        else:
            self.symbol = symbol

        self._end_date = Backtest.DEFAULT_END_DATE
        self._start_date = Backtest.DEFAULT_START_DATE
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
        date_val = _extract_date(date_param)

        if (date_val is not None) and (date_val < self.end_date):
            self._start_date = date_val
        else:
            raise ValueError("Invalid date or start_date > end_date.")

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, date_param):
        date_val = _extract_date(date_param)

        if (date_val is not None) and (date_val > self.start_date):
            self._end_date = date_val
        else:
            raise ValueError("Invalid date or end_date < start_date.")

    def download_prices(self):
        data = yf.download(self.symbol, self.start_date, self.end_date)
        self.data = data
