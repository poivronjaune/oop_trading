""" Symbols manager to extract and save information from inline sources """
import os
import datetime
import pandas as pd
from sqlalchemy import create_engine

# implement other sources
# https://firstratedata.com/b/22/stock-complete-historical-intraday
# https://eoddata.com/symbols.aspx


class OnlineSymbolsSource:
    """Base class to create targeted symbols extractors"""

    def __init__(self, url=None):
        """Attributes:
        url: Web source to use, no default
        symbols_df: Dataframe to store extracted symbols
        """
        self.name = "Undefined"
        self.url = url
        self.data = fake_data(0)

    def __repr__(self):
        return f"Name: {self.name}\nURL : {self.url}\n{self.data}\n"

    def scrap_symbols_from_source(self):
        """Method:
        Override method to implement extraction logic from source
        """
        raise NotImplementedError("Subclass must impleted this mehod")

    def to_sqlite(self, file_path=".", file_name="data.sqlite"):
        """Method:
            Save symbols dataframe to a sqlite database
        Params:
            file_path: defaults to current folder
            file_name: name of sqllite file to use as database, defaults to 'data.sqlite'
        """
        file_name = self.create_storage_folder_and_return_full_file_name(
            file_path, file_name
        )
        engine = create_engine(f"sqlite:///{file_name}")
        self.data.to_sql('Symbols', engine, if_exists='replace', index=False)

    def to_parquet(self, file_path=".", file_name="data.parquet"):
        """Method:
            Save symbols dataframe to a parquet file
        Params:
            file_path: defaults to current folder
            file_name: filename, defaults to 'data.parquet'
        """
        file_name = self.create_storage_folder_and_return_full_file_name(
            file_path, file_name
        )
        self.data.to_parquet(file_name, index=False)

    def to_csv(self, file_path=".", file_name="data.csv"):
        """Method:
            Save symbols dataframe to a csv file
        Params:
            file_path: defaults to current folder
            file_name: filename, defaults to 'data.csv'
        """
        file_name = self.create_storage_folder_and_return_full_file_name(
            file_path, file_name
        )
        self.data.to_csv(file_name, index=False, sep=";", mode="w")

    def create_storage_folder_and_return_full_file_name(self, file_path, file_name):
        """Create folder if non existent"""
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = os.path.join(file_path, file_name)
        return file_name


class FirstRateData(OnlineSymbolsSource):
    """First Rate Data symbol extractor implementation"""

    def __init__(self):
        url = "https://en.wikipedia.org/wiki/Stock_market"
        super().__init__(url=url)
        self.name = "First Rate Data"
        self.data = self.scrap_symbols_from_source()

    def scrap_symbols_from_source(self):
        data_df = fake_data(1)
        return data_df


def fake_data(set_index):
    """Fake Data to Test methods"""
    symbols_set_1 = [
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

    symbols_set_2 = [
        {
            "Symbol": "ZBID",
            "Name": "Bidon Added At The End",
            "ListedDt": datetime.datetime(2009, 6, 10).isoformat(),
            "LastDt": datetime.datetime(2022, 9, 6).isoformat(),
            "Status": "Test",
        }
    ]


    data_set = [symbols_set_1, symbols_set_2]
    symbols_df = pd.DataFrame(data_set[set_index]) if set_index in range(len(data_set)) else None

    return symbols_df


if __name__ == "__main__":
    df1 = FirstRateData()
    print(df1)
    df1.to_csv(file_path="tmp", file_name="test1.csv")
    df1.to_parquet(file_path="tmp", file_name="test1.parquet")
    df1.to_sqlite(file_path="tmp", file_name="test1.sqlite")
    