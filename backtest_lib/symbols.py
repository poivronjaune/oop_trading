# Single quotes are preferred '_' not "_"
from datetime import datetime
import os
import re
import requests
import dateutil
import pandas as pd

from sqlalchemy import create_engine

from bs4 import BeautifulSoup


class Symbols:
    def __init__(self):
        # Web scraping extraction parameters
        self.html = None
        self.source = "First Trade Data"
        self.line_marker = "First Date:"
        self.url = "https://firstratedata.com/b/22/stock-complete-historical-intraday"
        self.symbols_df = self._no_symbols_found()

        # Database storage parametrs
        self.db_name = "symbols.sqlite"
        self.db_columns = ['Symbol', 'Name', 'ListedDt', 'LastDt', 'Status']
        self.symbols_table_name = "Symbols"
        self.engine = None


    def build_symbols_dataframe(self):
        self.get_html_data_from_firstratedata_web_site()
        lines = self.extract_symbol_lines_from_html_content()
        self.convert_symbol_lines_to_dataframe(lines)
        self._update_symbols_listed_delisted_status()

    def get_html_data_from_firstratedata_web_site(self):
        html = requests.get(self.url).text
        if self.line_marker in html:
            self.html = requests.get(self.url).text
        else:
            self.html = None
            raise ValueError("Invalid web site.")

    def extract_symbol_lines_from_html_content(self):
        if self.html is None:
            self._no_symbols_found()
            return
        # This procedure is very sensitive to web site html layout
        # our tag to parse is the third one from last page <div>
        bs4_soup = BeautifulSoup(self.html, "html.parser")
        line = bs4_soup.find_all("div")
        line[-3].find()
        symbol_lines = []
        for line_element in line[-3]:
            if self.line_marker in line_element:
                symbol_str = str(line_element.string).strip().replace("  ", " ")
                symbol_lines.append(symbol_str)
        if len(symbol_lines) <= 0:
            symbol_lines = None

        return symbol_lines

    def convert_symbol_lines_to_dataframe(self, symbol_lines):
        # String format to convert: AA (Alcoa Corporation) First Date:18-Oct-2016 -> Last Date:31-Aug-2022
        # regx trick -> (?<=chars) start of matching string (lookbehind pattern not included in extraction)
        # regx trick -> (?=chars)  end of matching string   (lookahead pattern not included in extraction)

        if not isinstance(symbol_lines, list) or len(symbol_lines) <= 0:
            self._no_symbols_found()
            return

        regx_symbol_match = re.compile(r".+(?= \()")
        regx_name_match = re.compile(r"(?<=\().*(?=\))")
        regx_first_date_match = re.compile(r"(?<=First Date:).+(?= ->)")
        regx_last_date_match = re.compile(r"(?<=Last Date:).+")

        df = pd.DataFrame(columns=["Symbol", "Name", "ListedDt", "LastDt", "Status"])
        for line in symbol_lines:
            symbol = re.search(regx_symbol_match, line)
            symbol = "" if symbol is None else symbol.group()
            name = re.search(regx_name_match, line)
            name = "" if name is None else name.group()
            first_date = re.search(regx_first_date_match, line).group()
            last_date = re.search(regx_last_date_match, line).group()
            first_date_iso = dateutil.parser.parse(first_date).isoformat()
            last_date_iso = dateutil.parser.parse(last_date).isoformat()
            status = "Unknown"
            new_row = {
                "Symbol": [symbol],
                "Name": [name],
                "ListedDt": [first_date_iso],
                "LastDt": [last_date_iso],
                "Status": [status],
            }
            new_row_df = pd.DataFrame(new_row)
            df = pd.concat([df, new_row_df])

        self.symbols_df = df

    def _update_symbols_listed_delisted_status(self):
        df = self.symbols_df
        df.loc[~df.Symbol.str.contains("-DELISTED"), "Status"] = "Active"
        df.loc[df.Symbol.str.contains("-DELISTED"), "Status"] = "Delisted"
        df["Symbol"] = df["Symbol"].str.replace("-DELISTED", "")
        self.symbols_df = df

    def _no_symbols_found(self):
        self.symbols_df = None

    # DATABASE Functions
    def create_valid_db_name(self, db=None):
        if db is None:
            db_name = self.db_name
        else:
            db_name = db
        return db_name

    def create_db_engine(self, db=None):
        if db is None:
            db_name = self.db_name
        else:
            db_name = db

        engine = create_engine(f"sqlite:///{db_name}")
        self.engine = engine


    def load_symbols_from_db(self, db=None):
        db_name = self.create_valid_db_name(db)
        self.create_db_engine(db_name)
        stored_symbols = pd.read_sql(self.symbols_table_name, self.engine, index_col=None)
        return stored_symbols

    def merge_stored_and_new_symbols(self, stored_df, new_df):
        suffixe_new = '_new'
        cols_old = stored_df.columns
        cols_new = [f"{col}{suffixe_new}" for col in cols_old]
        cols_new[0] = cols_old[0]
        
        merged = pd.merge(stored_df, new_df, on='Symbol', how='outer', indicator=True, suffixes=['', '_new'])

        old_df = merged.loc[merged._merge == 'left_only'][cols_old]
        updates_df = merged.loc[merged._merge == 'both'][cols_new]
        updates_df.columns = cols_old
        new_sym_df = merged.loc[merged._merge == 'right_only'][cols_new]
        new_sym_df.columns = cols_old        
        
        updated_symbols = pd.concat([old_df, updates_df, new_sym_df], ignore_index=True)
        
        return updated_symbols

    def update_symbols_and_save(self, data, db=None):
        if data is not None:
            stored_symbols = self.load_symbols_from_db(db)
            updated_df = self.merge_stored_and_new_symbols(stored_symbols, data)
            self.save_symbols_to_db(data=updated_df, db=db)

    def save_symbols_to_db(self, data=None, db=None):
        db_name = self.create_valid_db_name(db)
        self.create_db_engine(db_name)
        if data is None:
            data_to_save = self.symbols_df
        else:
            data_to_save = data
        data_to_save.to_sql(self.symbols_table_name, self.engine, if_exists='replace', index=False)
