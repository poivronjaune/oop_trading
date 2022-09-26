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
