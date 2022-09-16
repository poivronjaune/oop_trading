import os
import pytest


def test_if_LOG_folder_exists():
    assert os.path.exists("log\\")


def test_if_all_packages_are_installed():
    # If package missing test run will not reach assert statement
    import yfinance
    import pandas
    import numpy
    import matplotlib
    import ta
    import bs4
    import sqlalchemy

    assert True
