from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


#sec.py
class ScrapeSICCodesFromSEC:
    def __call__(self):
        page = urlopen('http://www.sec.gov/info/edgar/siccodes.htm')
        soup = bs(page.read())
        table = soup.find_all('table')[2]
        table = table.find('table')
        trs = table.find_all('tr')[3:]
        for tr in trs:
            tds = tr.find_all('td')
            sic_code = tds[0].string
            sic_name = tds[-1].string.title()
            print(sic_code, sic_name)

s = ScrapeSICCodesFromSEC()
s()
