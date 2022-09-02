import re
import requests
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup, element


class Symbols:
    def __init__(self):
        self.html = None
        self.symbols_df = self.__no_symbols_found()

    def get_html_data_from_firstratedata_web_site(self):
        self.source = "First Trade Data"
        self.url = "https://firstratedata.com/b/22/stock-complete-historical-intraday"
        html = requests.get(self.url).text
        if "First Date:" in html:
            self.html = requests.get(self.url).text
        else:
            self.html = None

    def extract_symbols_from_web_page(self):
        if self.html is None:
            self.__no_symbols_found()
            return

        bs4_soup = BeautifulSoup(self.html, "html.parser")
        first_line_to_parse = self.__get_first_line_of_data_to_parse_from(bs4_soup)
        if first_line_to_parse is None:
            self.__no_symbols_found()
            return

        (
            listed_symbols_as_strings,
            delisted_symbols_as_strings,
        ) = self.__extract_symbol_lines_as_strings(first_line_to_parse)

        listed_df = self.__convert_strings_list_to_dataframe(listed_symbols_as_strings)

        self.symbols_df = listed_df  # TODO: merge listed symbols and delisted symbols as one Dataframe

    def __get_first_line_of_data_to_parse_from(self, bs4_soup):
        try:
            hrs_tags = bs4_soup.find_all("hr")
            if isinstance(hrs_tags, element.ResultSet) and len(hrs_tags) > 0:
                return hrs_tags[-1]
            else:
                return None
        except:
            return None

    def __extract_symbol_lines_as_strings(self, lines_to_parse):
        TEXT_MARKER = (
            "First Date:"  # Text to detect a line with symbols info in the soup
        )
        symbols_listed = []
        symbols_delisted = []
        line_element = lines_to_parse
        while line_element is not None:
            try:
                line_element = line_element.next
                if TEXT_MARKER in line_element:
                    symbol_str = str(line_element.string).strip().replace("  ", " ")
                    if "-DESLISTED" in symbol_str:
                        symbols_delisted.append(symbol_str.replace("-DELISTED", ""))
                    else:
                        symbols_listed.append(symbol_str)
            except:
                line_element = None

        return symbols_listed, symbols_delisted

    def __convert_strings_list_to_dataframe(self, symbols_str_list):
        # String format to convert: AA (Alcoa Corporation) First Date:18-Oct-2016 -> Last Date:31-Aug-2022
        # regx trick -> (?<=chars) start of matching string (lookbehind pattern not included in extraction)
        # regx trick -> (?=chars)  end of matching string   (lookahead pattern not included in extraction)

        if not isinstance(symbols_str_list, list) or len(symbols_str_list) <= 0:
            return None

        regx_symbol = re.compile(r".+(?= \()")
        regx_name = re.compile(r"(?<=\().+(?=\))")
        regx_first = re.compile(r"(?<=First Date:).+(?= ->)")
        regx_last = re.compile(r"(?<=Last Date:).+")

        symbol = re.search(regx_symbol, symbols_str_list[0]).group()
        name = re.search(regx_name, symbols_str_list[0]).group()
        first_date = re.search(regx_first, symbols_str_list[0]).group()
        last_date = re.search(regx_last, symbols_str_list[0]).group()

        symbols_df = pd.DataFrame()
        #new_df = pd.DataFrame([symbol, name, first_date, last_date])
        #symbols_df.append(new_df, ignore_index=True)
        symbols_df = pd.DataFrame(['one','two'])
        if len(symbols_df) <= 0:
            return None

        return symbols_df

    def __no_symbols_found(self):
        self.symbols_df = None
