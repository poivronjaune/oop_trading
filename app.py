""" Backtesting app for stock marketpartofolio automation """
from lib2to3.pygram import Symbols
import os
import sys

from stockmarket import symbols
from stockmarket.backtest import Backtest
from stockmarket.prices import Prices

from dashboard import Dashboard


def old_main():
    """Get price data, analyse trades, print chart and produce log file"""
    symbol = 'AAPL'
    try:
        backtest = Backtest(symbol)
        prices = Prices(symbol)
        prices.download_prices()
        backtest.data = prices.data
        del prices
    except RuntimeError as error_details:
        # AttributeError, RuntimeError
        print(f"\nError: {error_details}\n")
        return

    #backtest.add_indicators()

    print(backtest)
    print(backtest.data)


def main():
    data = {
        "exchanges": symbols.YAHOO_CODES
    }
    web_dash = Dashboard(data)
    web_dash.run()

if __name__ == "__main__":
    main()

