import os
import re
import requests
import dateutil
import pandas as pd

import sqlite3

from bs4 import BeautifulSoup


class Symbols:
    def __init__(self):
        self.html = None
        self.source = "First Trade Data"
        self.line_marker = "First Date:"
        self.url = "https://firstratedata.com/b/22/stock-complete-historical-intraday"
        self.symbols_df = self._no_symbols_found()

        self.db_name = "symbols.db"

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
            status = "Unknown"

            new_row = {
                "Symbol": [symbol],
                "Name": [name],
                "ListedDt": [dateutil.parser.parse(first_date)],
                "LastDt": [dateutil.parser.parse(last_date)],
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

    def save_symbols_to_db(self, db=None):
        # Saves or updates database
        if db is None:
            db_name = self.db_name
        else:
            db_name = db

        if os.path.exists(db_name):
            self.update_symbols_db(db_name)
        else:
            if self.symbols_df is not None and len(self.symbols_df) > 0:
                engine = sqlite3.connect(f"{db_name}")
                self.symbols_df.to_sql(db_name, engine, index=False)

    def update_symbols_db(self, db=None):
        if self.symbols_df is None:
            return

        if os.path.exists(db):
            engine = sqlite3.connect(f"{db}")
            c = engine.cursor()
            for row in self.symbols_df:
                print(row)
                symbol = row.symbol
                c.execute("SELECT * FROM 'symbols.db' WHERE Symbol = '{symbol}'")
                data = c.fetchone()
                if data is not None:
                    c.execute(f"UPDATE 'symbols.db' SET Name ='Temporary Name' WHERE Symbol = '{symbol}'")
                    engine.commit()
        else:
            raise ValueError("No DB found or Bad DB to update")


if __name__ == "__main__":
    print(f"Symbols app running....")
    instance = Symbols()
    instance.build_symbols_dataframe()
    print(instance.symbols_df.tail(10))
    

    # instance.build_symbols_dataframe()
    # print(f"{instance.symbols_df.tail(10)}")
    # instance.save_symbols_to_db()

    #engine = sqlite3.connect("symbols.db")
    #c = engine.cursor()
    ## c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #c.execute("SELECT * FROM 'symbols.db' WHERE symbol = 'AATCs'")
    #row = c.fetchone()
    #print(row)



    print(f"\nSymbols app terminated....")