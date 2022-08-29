import yfinance as yf

class Backtest:
    def __init__(self, symbol=None):
        self.symbol = 'AAPL'
        if symbol is not None:
            self.symbol = symbol

        df = yf.download(self.symbol)
        self.price_data = df

