from urllib import request
import requests
from bs4 import BeautifulSoup

class Symbols:
    def __init__(self):
        self.url = "https://firstratedata.com/b/22/stock-complete-historical-intraday"
        self.symbols_df = None

    def get_html_from_firstratedata_web_site(self):
        self.html = requests.get(self.url)

    