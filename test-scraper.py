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


import json
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

class ScrapeClassificationsFromZacks:
    def __call__(self):
        def parse_name(name):
            return name.strip('<span title="').split('"')[0]

        page = urlopen('http://www.zacks.com/zrank/sector-industry-classification.php')
        soup = bs(page.read())
        main_body = soup.find('div', {'class': 'main_body'})
        script = main_body.find('script')
        string = str(script).split('"data"  : ')[-1]
        string = string.rstrip('}</script>').strip().rstrip()
        string = re.sub('{', '[{', string)
        string = re.sub('}', '}]', string)

        json_data = json.loads(string)

        for group in json_data:
            group_dict = group[0]

            sector_name = parse_name(group_dict['Sector Group'])
            sector_code = group_dict['Sector Code']
            print('sector', sector_code, sector_name)

            industry_name = parse_name(group_dict['Medium(M) Industry Group'])
            industry_code = group_dict['Medium(M) Industry Code']
            print('industry', industry_code, industry_name)

            segment_name = parse_name(group_dict['Expanded(X) Industry Group'])
            segment_code = group_dict['Expanded(X) Industry Code']
            print('segment', segment_code, segment_name)

s = ScrapeClassificationsFromZacks()
s()
