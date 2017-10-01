from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


#sec.py
class ScrapeSICCodesFromSEC:
    def __call__(self):
        page = urlopen('http://fortune.com/2017/09/27/term-sheet-tuesday-september-26/')
        soup = bs(page.read(), "lxml")
        h2s = soup.find_all('h2')
        for h2 in h2s:
            print(h2.string)

s = ScrapeSICCodesFromSEC()
s()
