import pytest
from backtesting import Backtest

def test_instantiate_backtest_class():
    try:
        instance = Backtest()
        assert True
    except:
        assert False

def test_backtest_default_symbol_is_AAPL():
    instance = Backtest()
    assert instance.symbol == 'AAPL'

@pytest.mark.parametrize('symbol', ['TSLA', 'MSFT'])
def test_backtest_loads_data_for_symbol(symbol):
    instance = Backtest(symbol)
    assert instance.symbol == symbol
