import sys

from backtesting import Backtest

def argv_parse():
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
    else:
        symbol = 'AAPL'
    if len(sys.argv) > 2:
        log_file = sys.argv[2]
    else:
        log_file = 'trades.csv'
    return symbol, log_file

def main():
    symbol, log_file = argv_parse()
    try:
        instance = Backtest(symbol)
    except Exception as e:
        print(f"\nError: {e}\n")
        return

    # print(f"Symbol: {instance.symbol}")
    # print(f"Prices: {instance.df}")
    # print(f"Buy prices: {instance.buy_arr}")
    # print(f"Sell prices: {instance.sell_arr}")
    # print(f"Profit per trade: {instance.profit}")
    # print(f"Cumulative profit: {instance.cumulative_profit}")

    instance.plot_chart()
    instance.log_trades(file=log_file)

if __name__ == '__main__':
    main()