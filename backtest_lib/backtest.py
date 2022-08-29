from datetime import datetime, timedelta
import yfinance as yf


class Backtest:
    def __init__(self, symbol=None):
        if symbol == None:
            self._symbol = "AAPL"
        else:
            self.symbol = symbol

        self.start_date = datetime(2018, 1, 1)
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
            raise ValueError("Invalid stock symbol.")

    def download_prices(self):
        data = yf.download(self.symbol, self.start_date, self.end_date)
        self.data = data
