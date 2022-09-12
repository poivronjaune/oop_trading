import os
import datetime
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
    symbols_data = [
        {
            "Symbol": "A",
            "Name": "Agilent Technologies Inc",
            "ListedDt": datetime.datetime(2005, 1, 3).isoformat(),
            "LastDt": datetime.datetime(2022, 9, 6).isoformat(),
            "Status": "Active",
        },
        {
            "Symbol": "AA",
            "Name": "Alcoa Corporation",
            "ListedDt": datetime.datetime(2016, 10, 18).isoformat(),
            "LastDt": datetime.datetime(2022, 9, 6).isoformat(),
            "Status": "Active",
        },
        {
            "Symbol": "ZGNX",
            "Name": "Zogenix",
            "ListedDt": datetime.datetime(2010, 11, 23).isoformat(),
            "LastDt": datetime.datetime(2022, 3, 4).isoformat(),
            "Status": "Active",
        },
    ]

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
        bad_symbols = [
            symbol
            for symbol in instance.symbols_df.Symbol.tolist()
            if "-DELISTED" in symbol
        ]
        assert "Unknown" not in status_values
        assert len(bad_symbols) == 0

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
    def test_real_save(self):
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        instance.build_symbols_dataframe()
        instance.save_symbols_to_db('tmp/real.db')
        assert os.path.exists('tmp/real.db')

    def test_save_symbols_to_db(self):
        instance = Symbols()
        data = TestSymbolsClass.symbols_data
        instance.symbols_df = pd.DataFrame(data)
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        tmp_db = r"tmp\symbols.db"
        instance.save_symbols_to_db(tmp_db)
        assert os.path.exists(tmp_db)

    def test_update_symbols_db_no_data(self):
        instance = Symbols()
        instance.update_symbols_db(db=r"tmp\empty.db")
        assert not os.path.exists(r"tmp\empty.db")

    def test_update_valid_symbols_db(self):
        # Must have run test_save_symbols_to_db() prior to this test
        #data = TestSymbolsClass.symbols_data
        instance = Symbols()
        instance.get_html_data_from_firstratedata_web_site()
        instance.build_symbols_dataframe()

        data = instance.symbols_df
        new_row = pd.DataFrame(
            [
                {
                    "Symbol": "ZBID",
                    "Name": "Bidon Added At The End",
                    "ListedDt": datetime.datetime(2009, 6, 10).isoformat(),
                    "LastDt": datetime.datetime(2022, 9, 6).isoformat(),
                    "Status": "Test",
                }
            ]
        )
        data_df = pd.concat([pd.DataFrame(data), new_row], ignore_index=True)
        instance = Symbols()
        instance.symbols_df = data_df
        instance.update_symbols_db(r"tmp\symbols.db")