from datetime import datetime
import pytest

from backtest_lib.backtest import Backtest


def test_always_True():
    assert True


def test_backtest_init_valid():
    # Make sure defaults are set at class creation
    instance = Backtest()
    assert instance is not None
    assert instance.symbol == "AAPL"
    assert instance.start_date == datetime(2018, 1, 1)
    assert instance.end_date == datetime.now()
    assert instance.data == None


def test_Backtest_symbol_stores_only_first_value():
    instance = Backtest("TSLA MSFT")
    assert instance.symbol == "TSLA"
    instance = Backtest("TSLA,MSFT")
    assert instance.symbol == "TSLA"
    instance = Backtest(["TSLA", "MSFT"])
    assert instance.symbol == "TSLA"


def test_Backtest_data_check_prices_column_structure():
    instance = Backtest()
    instance.download_prices()

    index_name = "Date"
    columns_names = ["Open", "Close", "High", "Low", "Volume"]
    assert instance.data.index.name == index_name
    assert instance.data.columns.all() in columns_names
    

def test_Backtest_data_prices_data_has_downloaded_values():
    instance = Backtest("TSLA MSFT")
    instance.download_prices()
    assert len(instance.data) > 0
