""" Backtesting app for stock marketpartofolio automation """
import os
import sys

from backtest_lib.backtest import Backtest


def argv_parse():
    """Command line options: [1] symbol, [2] log file name"""
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
        instance = Backtest(symbol)
    except RuntimeError as error_details:
        # AttributeError, RuntimeError
        print(f"\nError: {error_details}\n")
        return


if __name__ == "__main__":
    main()
