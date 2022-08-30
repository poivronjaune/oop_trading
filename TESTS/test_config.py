import os


def test_if_LOG_folder_exists():
    assert os.path.exists("log\\")


def test_if_all_packages_are_installed():
    import yfinance
    import pandas
    import numpy
    import matplotlib
    import ta

    assert True
