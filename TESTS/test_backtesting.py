import pytest
from backtesting.backtesting import Backtest


def test_instantiate_backtest_class():
    try:
        instance = Backtest()
        assert True
    except:
        assert False


def test_backtest_default_symbol_is_AAPL():
    instance = Backtest()
    assert instance.symbol == "AAPL"


@pytest.mark.parametrize("symbol", ["TSLA", "MSFT", "AMZN"])
def test_backtest_loads_data_for_symbol(symbol):
    instance = Backtest(symbol)
    assert instance.symbol == symbol


@pytest.mark.parametrize("bad_symbol", ["TSLAbad", "MSFTbad", "badAMZN"])
def test_backtest_did_not_load_data_for_symbol(bad_symbol):
    with pytest.raises(ValueError):
        instance = Backtest(bad_symbol)


@pytest.mark.parametrize("symbol", ["TSLA", "MSFT", "AMZN"])
def test_symbol_price_data_returned(symbol):
    instance = Backtest(symbol)
    if instance.df.size > 1:
        assert True
    else:
        assert False


def test_if_dataframe_has_OHLCV_columns():
    instance = Backtest()
    valid_columns = True
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        valid_columns = valid_columns & (c in instance.df.columns.tolist())
    assert valid_columns


def test_if_calc_indicators_added_some_new_columns():
    instance = Backtest()
    valid_columns = True
    for c in ["ma_20", "upper_bb", "rsi"]:
        valid_columns = valid_columns & (c in instance.df.columns.tolist())
    assert valid_columns


def test_if_generate_signals_added_strategy_signal_column():
    instance = Backtest()
    assert "signal" in instance.df.columns.tolist()
