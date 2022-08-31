from backtest_lib.symbols import Symbols


class TestSymbolsClass:
    def test_Symbols_valide_instance(self):
        instance = Symbols()
        assert instance is not None
        assert instance.symbols_df == None
        # assert instance.start_date == Backtest.DEFAULT_START_DATE
        # assert instance.end_date == Backtest.DEFAULT_END_DATE
        # assert instance.data == None

    def test_get_html_from_web(self):
        instance= Symbols()
        instance.get_html_from_firstratedata_web_site()
        assert instance.html is not None
        assert instance.html.ok

    