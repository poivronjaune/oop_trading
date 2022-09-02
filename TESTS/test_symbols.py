import pytest
import pandas as pd
from backtest_lib.symbols import Symbols


class TestSymbolsClass:
    def test_Symbols_valid_instance(self):
        instance = Symbols()
        assert instance is not None
        assert instance.html == None
        assert instance.symbols_df == None
        # assert instance.start_date == Backtest.DEFAULT_START_DATE
        # assert instance.end_date == Backtest.DEFAULT_END_DATE
        # assert instance.data == None

    def test_get_html_data_from_firstratedata_web_site(self):
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        assert instance.html is not None
        
    def test_extract_symbols_from_web_page_NO_WEBPAGE(self):
        instance = Symbols()
        instance.extract_symbols_from_web_page()
        assert instance.symbols_df is None

    def test_extract_symbols_from_web_page(self):
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        instance.extract_symbols_from_web_page()
        assert instance.symbols_df is not None
        assert isinstance(instance.symbols_df, pd.core.frame.DataFrame)
        assert len(instance.symbols_df) > 0