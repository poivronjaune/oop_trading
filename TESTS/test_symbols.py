import os
from modulefinder import Module
from msilib.schema import Class
import pytest
import pandas as pd
from bs4 import BeautifulSoup, element
from backtest_lib.symbols import Symbols


class TestSymbolsClass:
    #
    # Test functions to extract data from web site
    #
    def test_Symbols_valid_instance(self):
        instance = Symbols()
        assert instance is not None
        assert instance.html == None
        assert instance.symbols_df == None
        assert instance.line_marker == "First Date:"
        assert instance.source == "First Trade Data"

    def test_get_html_data_from_firstratedata_web_site(self):
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        assert instance.html is not None

    def test_extract_symbol_lines_from_html_content_using_default_line_marker(self):
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        symbols_list = instance.extract_symbol_lines_from_html_content()
        symbols_list = instance.extract_symbol_lines_from_html_content()
        assert symbols_list is not None
        assert instance.line_marker in symbols_list[0]

    def test_convert_symbol_lines_to_dataframe(self):
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        symbol_lines = instance.extract_symbol_lines_from_html_content()
        instance.convert_symbol_lines_to_dataframe(symbol_lines)
        assert isinstance(instance.symbols_df, pd.DataFrame)
        assert len(instance.symbols_df) > 0

    def test_update_symbols_listed_delisted_status(self):
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        symbol_lines = instance.extract_symbol_lines_from_html_content()
        instance.convert_symbol_lines_to_dataframe(symbol_lines)
        instance._update_symbols_listed_delisted_status()
        status_values = instance.symbols_df.Status.tolist()
        assert "Unknown" not in status_values

    def test_build_symbols_dataframe(self):
        instance = Symbols()
        instance.build_symbols_dataframe()
        assert instance.symbols_df is not None
        assert isinstance(instance.symbols_df, pd.DataFrame)
        assert "unknown" not in instance.symbols_df.Status.tolist()

    #
    # test for ERROR conditions
    #
    def test_get_html_data_from_bad_web_site(self):
        instance = Symbols()
        instance.url = "bad url"
        with pytest.raises(Exception):
            instance.get_html_data_from_firstratedata_web_site()

    def test_get_html_data_from_web_site_no_line_marker_found(self):
        instance = Symbols()
        instance.url = "https://en.wikipedia.org/wiki/Stock_market"
        with pytest.raises(Exception):
            instance.get_html_data_from_firstratedata_web_site()

    def test_no_html_returned_to_extract_from(self):
        instance = Symbols()
        instance.html = None
        instance.extract_symbol_lines_from_html_content()
        assert instance.symbols_df is None

    def test_no_symbols_found_in_html_page(self):
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        instance.line_marker = "Bad marker"
        instance.extract_symbol_lines_from_html_content()
        assert instance.symbols_df is None

    def test_convert_symbol_lines_to_dataframe_bad_list(self):
        instance = Symbols()
        symbol_lines = "not a list type"
        instance.convert_symbol_lines_to_dataframe(symbol_lines)
        assert instance.symbols_df is None

    #
    # Test functions for Databases
    #
    def test_save_symbols_to_db(self):
        instance = Symbols()
        instance.build_symbols_dataframe()
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        tmp_db ='tmp\symbols1.db'
        instance.save_symbols_to_db(tmp_db)
        assert os.path.exists(tmp_db)
        