""" Backtesting app for stock marketpartofolio automation """
import os
import sys

from backtest_lib.symbols import SymbolsSource
from backtest_lib.backtest import Backtest
from backtest_lib.prices import Prices

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
    web_dash = Dashboard()
    web_dash.run()

if __name__ == "__main__":
    main()
