from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
from dateutil import parser

BASE_URL = "http://fortune.com/"
TRAILING_SLASH = "/"
HYPHEN = "-"
TERM_SHEET = "term-sheet-"
BLACKLIST_DAYS = set(["Saturday","Sunday"])

# class ScrapeFromFortune:
#     def __call__(self):
#         page = urlopen('http://fortune.com/2017/09/27/term-sheet-tuesday-september-26/')
#         soup = bs(page.read(), "lxml")
#         h2s = soup.find_all('h2')
#         for h2 in h2s:
#             print(h2.string)
#
# s = ScrapeFromFortune()
# s()

def generateURLs():
    d1 = date(2011,3, 11)  # start date
    d2 = date.today()
    delta = d2 - d1         # timedelta
    urls = []
    for i in range(delta.days + 1):
        currentDate = d1 + timedelta(days=i)
        currentDateString = currentDate.strftime('%Y-%m-%d')
        day = parser.parse(currentDateString).strftime("%A")
        if day in BLACKLIST_DAYS :
            continue
        month = parser.parse(currentDateString).strftime("%B")
        dateParts = currentDateString.split(HYPHEN)
        url = BASE_URL + dateParts[0] + TRAILING_SLASH + dateParts[1] + TRAILING_SLASH + dateParts[2].lstrip("0") + TRAILING_SLASH + TERM_SHEET + day.lower() + HYPHEN + month.lower() + HYPHEN + dateParts[2].lstrip("0") + TRAILING_SLASH
        urls.insert( i, url )
        print (url)
    return urls

generateURLs()
