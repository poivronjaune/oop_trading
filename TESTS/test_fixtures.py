import pytest
import requests
from bs4 import BeautifulSoup

@pytest.mark.skip
class TestHtmlContent:
    url = 'http://web.simmons.edu/~grovesd/comm244/notes/week3/html-test-page.html'
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, 'html.parser')

    def test_always_true(self):
        print(f'\nAlways true')
        True

    def test_title_is_original(self):
        soup = TestHtmlContent.soup        
        assert soup.find('title').string == 'HTML Page for Testing CSS'

    def test_title_changed(self):
        soup = TestHtmlContent.soup
        print(f'\nInitial title value: {soup.find("title").string}')
        soup.title.string = 'New title'
        print(f'Changed title value: {soup.find("title").string}')
        assert soup.find('title').string == 'New title'

    def test_title_after_changed(self):
        soup = TestHtmlContent.soup
        assert soup.find('title').string == 'HTML Page for Testing CSS'