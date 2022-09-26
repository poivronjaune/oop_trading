""" Symbols manager to extract and save information from inline sources """
from msilib.schema import Class
import os
import re
import string
import datetime
import dateutil
import requests
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from bs4 import BeautifulSoup

# implement other sources
# https://firstratedata.com/b/22/stock-complete-historical-intraday
# https://eoddata.com/symbols.aspx


class SymbolsSource:
    """Base class to create targeted symbols extractors
    Param:
        url: Web source of symbol data to scrape
    Usage:
        Instantiate object, then call .scrape_symbols_from_source()    
    """

    def __init__(self, url=None):
        """Attributes:
        url: Web source to use, no default
        symbols_df: Dataframe to store extracted symbols
        """
        self.name = "Generic Name"
        self.url = url
        self.exchange = ''
        self.yahoo_suffix = ''        
        self.data = None


    def __repr__(self):
        str_items_in_data = "Empty" if self.data is None else f"{len(self.data)} items"

        info_to_str = f"\nClass attributes:\n"
        info_to_str += f"class        : {type(self).__name__} <- {self.__class__.__bases__[0].__name__}\n"
        info_to_str += f"name         : {self.name}\n"
        info_to_str += f"exchange     : {self.exchange}\n"
        info_to_str += f"url          : {self.url}\n"
        info_to_str += f"yahoo_suffix : {'None' if self.yahoo_suffix == '' else self.yahoo_suffix}\n"
        info_to_str += f"data         : {str_items_in_data}\n"
        
        #f"Name: {self.name}\nURL : {self.url}\n{self.data}\n"
        return info_to_str

    def scrape_symbols_from_source(self):
        """Method:
            Abstract method needs to be implemented in subclass as extraction logic from source
        """
        raise NotImplementedError("Subclass must impleted this mehod")

    def augment_symbol_with_yahoo_info(self, symbol_serie):
        yahoo_ticker = f"{symbol_serie.Symbol}{self.yahoo_suffix}"
        yahoo = yf.Ticker(yahoo_ticker)
        symbol_info = symbol_serie.to_dict()
        if yahoo:
            yahoo_info = {
                'Sector': yahoo.info.get('sector'),
                'Industry': yahoo.info.get('industry'),
                'Type': yahoo.info.get('quoteType'),
                'Source': yahoo.info.get('quoteTypeSourceName'),
                'Website': yahoo.info.get('website'),
                'LogoUrl': yahoo.info.get('logo_url'),
                'Exchange': yahoo.info.get('exchange'),
                'ShortName': yahoo.info.get('shortName'),
                'LongName': yahoo.info.get('longName'),
                'Market': yahoo.info.get('market'),
                'FundFamily': yahoo.info.get('fundFamily'),
                'MarketCapValue': yahoo.info.get('marketCap'),
                'YahooTicker': yahoo_ticker,
                'ExchangeCode': self.exchange
                }
        else:
            yahoo_info = {
                'Sector': '',
                'Industry': '',
                'Type': '',
                'Source': '',
                'Website': '',
                'LogoUrl': '',
                'Exchange': '',
                'ShortName': '',
                'LongName': '',
                'Market': '',
                'FundFamily': '',
                'MarketCapValue': '',
                'YahooTicker': yahoo_ticker,
                'ExchangeCode': self.exchange
                }
        #yahoo_serie = pd.Series(yahoo_info)
        #augmented_serie = pd.concat([symbol_serie, yahoo_serie])
        augmented_dict = symbol_info | yahoo_info
        return augmented_dict

    def augment_symbols_to_csv(self, file_path=".", file_name="augmented.csv"):
        # load existing augmented file/data
        # find first occurence of symbol info without augmented flag
        # loop from this point to add agmented info
        # save augmented files

        file_name = self.create_storage_folder_and_return_full_file_name(file_path, file_name)
        for i in range(0, len(self.data)):
            augmented_dict = self.augment_symbol_with_yahoo_info(self.data.iloc[i])
            print(f"i:{i} / {len(self.data)} ===============================")
            print(type(augmented_dict))
            print(augmented_dict)
            print("=========================================================")
            augmented_df = pd.DataFrame([augmented_dict])
            #filename = 'data/augmented.csv'
            if os.path.exists(file_name):
                augmented_df.to_csv(file_name, header=False, index=False, mode='a')
            else:
                augmented_df.to_csv(file_name, header=True, index=False, mode='a')


    def load_from_csv(self, file_path=".", file_name="data.csv"):
        data_df = pd.read_csv(os.path.join(file_path, file_name), index_col=False)
        self.data = data_df

    def load_from_parquet(self, file_path=".", file_name="data.parquet"):
        data_df = pd.read_parquet(os.path.join(file_path, file_name))
        self.data = data_df

    def load_from_sqlite(self, file_path=".", file_name="data.parquet"):
        engine = engine = create_engine(f"sqlite:///{os.path.join(file_path, file_name)}")
        data_df = pd.read_sql('Symbols', engine, index_col=None)
        self.data = data_df

    def to_sqlite(self, file_path=".", file_name="data.sqlite"):
        """Method:
            Save symbols dataframe to a sqlite database
        Params:
            file_path: defaults to current folder
            file_name: name of sqllite file to use as database, defaults to 'data.sqlite'
        """
        file_name = self.create_storage_folder_and_return_full_file_name(file_path, file_name)
        engine = create_engine(f"sqlite:///{file_name}")
        self.data.to_sql("Symbols", engine, if_exists="replace", index=False)

    def to_parquet(self, file_path=".", file_name="data.parquet"):
        """Method:
            Save symbols dataframe to a parquet file
        Params:
            file_path: defaults to current folder
            file_name: filename, defaults to 'data.parquet'
        """
        file_name = self.create_storage_folder_and_return_full_file_name(file_path, file_name)
        self.data.to_parquet(file_name, index=False)

    def to_csv(self, file_path=".", file_name="data.csv"):
        """Method:
            Save symbols dataframe to a csv file
        Params:
            file_path: defaults to current folder
            file_name: filename, defaults to 'data.csv'
        """
        file_name = self.create_storage_folder_and_return_full_file_name(file_path, file_name)
        self.data.to_csv(file_name, index=False, sep=",", mode="w")

    def create_storage_folder_and_return_full_file_name(self, file_path, file_name):
        """Method:
            Create folder if non existent and return full path and filename
        Params:
            file_path: required parameter
            file_name: required parameter
        """
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = os.path.join(file_path, file_name)
        return file_name

    def save_all_formats(self, file_path='tmp', file_name_no_ext='data'):
        file_name = f"eoddata_{file_name_no_ext.lower()}"
        self.to_csv(file_path=file_path, file_name=f"{file_name}.csv")
        self.to_parquet(file_path=file_path, file_name=f"{file_name}.parquet")
        self.to_sqlite(file_path=file_path, file_name=f"{file_name}.sqlite")    


class FirstRateData(SymbolsSource):
    """First Rate Data symbol extractor implementation
        Instantiate object, then call .scrape_symbols_from_source
    """
    LINE_MARKER = 'First Date:'
    URL = "https://firstratedata.com/b/22/stock-complete-historical-intraday"

    def __init__(self, url=None):
        ''' '''
        super().__init__(url=self.URL)
        self.name = "First Rate Data"
        self.exchange = 'NASDAQ'


    def scrape_symbols_from_source(self):
        ''' Method:
            Open web source and scrape symbols strings to build a data DataFrame
        '''
        html = self.get_html_content(self.url)
        strings = self.extract_raw_symbol_strings(html)
        symbols_df = self.convert_strings_to_dataframe(strings)
        symbols_df = self.fix_symbols_status(symbols_df)

        self.data = symbols_df

    def get_html_content(self, url):
        ''' Helper method to obtain raw source data '''
        try:
            res = requests.get(url, timeout=15)
        except:
            raise ValueError('Invalid request to web site')
        
        html = None
        if FirstRateData.LINE_MARKER in res.text:
            html = res.text

        if html is None:
            raise ValueError("Invalid web site.")

        return html

    def extract_raw_symbol_strings(self, html):
        '''Extract raw string that contain LINE_MARKER from html content'''
        if html is None:
            return None

        bs4_soup = BeautifulSoup(html, "html.parser")
        div_elements_to_extract_from = bs4_soup.find_all("div")[-3]
        symbol_lines = []
        for line_element in div_elements_to_extract_from:
            if FirstRateData.LINE_MARKER in line_element:
                symbol_str = str(line_element.string).strip().replace("  ", " ")
                symbol_lines.append(symbol_str)

        if len(symbol_lines) <= 0:
            symbol_lines = None

        return symbol_lines

    def convert_strings_to_dataframe(self, symbol_lines):
        '''Helper function to transform strings of symbol info to a dataframe'''
        # pylint: disable=line-too-long
        if not isinstance(symbol_lines, list) or len(symbol_lines) <= 0:
            return None

        data_df = pd.DataFrame(columns=["Symbol", "Name", "ListedDt", "LastDt", "Status"])
        for line in symbol_lines:
            symbol = self.extract_text_from_string(line, re.compile(r".+(?= \()"))
            name = self.extract_text_from_string(line, re.compile(r"(?<=\().*(?=\))"))
            first_date = self.extract_text_from_string(line, re.compile(r"(?<=First Date:).+(?= ->)"))
            first_date = dateutil.parser.parse(first_date).isoformat()
            last_date = self.extract_text_from_string(line, re.compile(r"(?<=Last Date:).+"))
            last_date = dateutil.parser.parse(last_date).isoformat()

            new_row = {
                "Symbol": [symbol],
                "Name": [name],
                "ListedDt": [first_date],
                "LastDt": [last_date],
                "Status": "Unknown",
            }
            new_row_df = pd.DataFrame(new_row)
            data_df = pd.concat([data_df, new_row_df])
        # pylint: enable=line-too-long
        return data_df

    def fix_symbols_status(self, data_df):
        '''Update Status of symbol info and removed -DELISTED text from symbol_code'''
        data_df.loc[~data_df.Symbol.str.contains("-DELISTED"), "Status"] = "Active"
        data_df.loc[data_df.Symbol.str.contains("-DELISTED"), "Status"] = "Delisted"
        data_df["Symbol"] = data_df["Symbol"].str.replace("-DELISTED", "")
        return data_df

    def extract_text_from_string(self, line_str, regx_match):
        '''Helper function to extract regx pattern from a string line'''
        symbol_code = re.search(regx_match, line_str)
        symbol_code = "" if symbol_code is None else symbol_code.group()
        return symbol_code

class EndOfDayData(SymbolsSource):
    """EODData symbol extractor implementation
        Instantiate object, then call .scrape_symbols_from_source
    """
    URL = 'https://eoddata.com/stocklist'
    VALID_EXCHANGES = ['NASDAQ', 'AMEX','ASX','LSE','NYSE','SGX','TSX','TSXV']

    YAHOO_CODES = [
        {'Code': 'NASDAQ', 'Name':'NASDAQ Stock Exchange', 'Country':'USA', 'Suffix':''},
        {'Code': 'AMEX', 'Name':'American Stock Exchange', 'Country':'USA', 'Suffix':''},
        {'Code': 'ASX', 'Name':'Australian Stock Exchange', 'Country':'Australia', 'Suffix':'.AX'},
        {'Code': 'LSE', 'Name':'London Stock Exchange', 'Country':'United Kingdom', 'Suffix':'.L'},
        {'Code': 'NYSE', 'Name':'New York Stock Exchange', 'Country':'USA', 'Suffix':''},
        {'Code': 'SGX', 'Name':'Singapore Stock Exchange', 'Country':'Republic of Singapore', 'Suffix':'.SI'},
        {'Code': 'TSX', 'Name':'Toronto Stock Exchange', 'Country':'Canada', 'Suffix':'.TO'},
        {'Code': 'TSXV', 'Name':'Toronto Venture Exchange', 'Country':'Canada', 'Suffix':'.V'},
    ]



    def __init__(self, exchange='NASDAQ'):
        if exchange not in EndOfDayData.VALID_EXCHANGES:
            raise ValueError('Unsupported Exchange value')

        url = self.build_url(self.URL, exchange, 'A')
        super().__init__(url=url)
        self.name = 'End Of Day Data'
        self.exchange = exchange
        self.yahoo_suffix = [l for l in EndOfDayData.YAHOO_CODES if l.get('Code') == exchange][0].get('Suffix')
        #self.data = self.scrape_symbols_from_source()

    def scrape_symbols_from_source(self):
        letters = list(string.ascii_uppercase) + list(string.digits)
        data_df = pd.DataFrame()
        for letter in letters:
            url = self.build_url(EndOfDayData.URL, self.exchange, letter)
            page_data = self.scrape_one_page(url)
            data_df = pd.concat([data_df, page_data], ignore_index=True)

        data_df.drop_duplicates(subset='Symbol', keep='first', inplace=True)
        
        self.data = data_df

    def scrape_one_page(self, url):
        symbols_data = pd.read_html(url)
        symbols_data = symbols_data[4]
        symbols_data = symbols_data[['Code','Name']]
        symbols_data.columns = ["Symbol", "Name"]
        return symbols_data

    def build_url(self, url, exchange, letter):
        return f"{url}/{exchange}/{letter}.htm"


def fake_data(set_index):
    """Fake Data to Test methods, pass a number to choose the dataset"""
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
    symbols_df = (
        pd.DataFrame(data_set[set_index]) if set_index in range(len(data_set)) else None
    )

    return symbols_df


if __name__ == "__main__":
    # df0 = OnlineSymbolsSource()
    # print(df0)

    #df1 = FirstRateData()
    #print(df1)
    #df1.scrape_symbols_from_source()
    #print(df1)
    #res = df1.augment_symbols_data()
    #print(type(res))
    #print(res)

    # ['NASDAQ', 'AMEX','ASX','LSE','NYSE','SGX','TSX','TSXV']
    df2 = EndOfDayData('AMEX')
    print(df2)
    df2.scrape_symbols_from_source()
    print(df2)
    res = df2.augment_symbols_to_csv('data','amex-augmented.csv')
    print(type(res))
    print(res)
    
    