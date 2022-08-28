import os
import pytest


def test_if_LOG_folder_exists():
    assert os.path.exists("log\\")


# Is this necessary? Why not use a @mark.parametrize() or load requirements.txt and loop though
def test_if_package_installed_yfinance():
    try:
        import yfinance

        assert True
    except:
        assert False


def test_if_package_installed_pandas():
    try:
        import pandas

        assert True
    except:
        assert False


def test_if_package_installed_numpy():
    try:
        import numpy

        assert True
    except:
        assert False


def test_if_package_installed_matplotlib():
    try:
        import matplotlib

        assert True
    except:
        assert False


def test_if_package_installed_ta():
    try:
        import ta

        assert True
    except:
        assert False
