""" Backtesting app for stock marketpartofolio automation """
import os
import sys

from stockmarket.symbols import SymbolsSource
from stockmarket.backtest import Backtest
from stockmarket.prices import Prices


def argv_parse():
    """Command line options: py app.py <symbol> <log file>"""
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
    else:
        symbol = "AAPL"

    if len(sys.argv) > 2:
        log_file = sys.argv[2]
    else:
        log_file = "trades.csv"

    return symbol, log_file


def main():
    """Get price data, analyse trades, print chart and produce log file"""
    symbol, log_file = argv_parse()
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


if __name__ == "__main__":
    main()
