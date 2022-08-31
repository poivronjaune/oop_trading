from datetime import datetime
import pytest

from backtest_lib.backtest import Backtest


def test_always_True():
    assert True


def test_Backtest__init__valid():
    # Make sure defaults are set at class creation
    instance = Backtest()
    assert instance is not None
    assert instance.symbol == Backtest.DEFAULT_SYMBOL
    assert instance.start_date == Backtest.DEFAULT_START_DATE
    assert instance.end_date == Backtest.DEFAULT_END_DATE
    assert instance.data == None


class TestBacktestSymbols:
    @pytest.mark.parametrize(
        "symbol", ["TSLA", "TSLA MSFT", "TSLA,MSFT", ["TSLA", "MSFT"]]
    )
    def test_Backtest_symbol_stores_only_first_value(self, symbol):
        instance = Backtest(symbol)
        assert instance.symbol == "TSLA"
        # instance = Backtest("TSLA,MSFT")
        # assert instance.symbol == "TSLA"
        # instance = Backtest(["TSLA", "MSFT"])
        # assert instance.symbol == "TSLA"

    def test_Backtest_if_symbol_empty_store_default_value(self):
        with pytest.raises(ValueError):
            instance = Backtest(" ")


class TestBacktestStartDate:
    def test_start_date_set_from_a_string(self):
        instance = Backtest()
        instance.start_date = "2020-01-23"
        assert instance.start_date == datetime(2020, 1, 23)

    @pytest.mark.parametrize("bad_str_date", ["2022-01-33", "bad_str"])
    def test_start_date_set_from_invalid_str_date(self, bad_str_date):
        instance = Backtest()
        with pytest.raises(ValueError):
            instance.start_date = bad_str_date

    def test_start_date_from_a_datetime_value(self):
        instance = Backtest()
        new_date = datetime(2020, 1, 23)
        instance.start_date = new_date
        assert instance.start_date == new_date

    def test_start_date_greater_than_end_date(self):
        instance = Backtest()
        instance.end_date = datetime(2021, 1, 1)
        with pytest.raises(ValueError):
            instance.start_date = "2022-01-01"


class TestBacktestEndDate:
    def test_end_date_smaller_than_start_date(self):
        instance = Backtest()
        instance.start_date = "2022-01-01"
        with pytest.raises(ValueError):
            instance.end_date = "2020-01-01"


class TestBacktest_Data:
    def test_Backtest_data_check_prices_column_structure(self):
        instance = Backtest()
        instance.download_prices()

        index_name = "Date"
        columns_names = ["Open", "Close", "High", "Low", "Volume"]
        assert instance.data.index.name == index_name
        assert instance.data.columns.all() in columns_names

    def test_data_does_not_have_multi_level(self):
        instance = Backtest()
        instance.download_prices()
        assert instance.data.index.nlevels == 1
        assert instance.data.columns.nlevels == 1

    @pytest.mark.parametrize("symbol", ["TSLA", "TSLA MSFT", "TSLA,MSFT"])
    def test_Backtest_data_prices_data_has_downloaded_values(self, symbol):
        instance = Backtest(symbol)
        instance.download_prices()
        assert len(instance.data) > 0
