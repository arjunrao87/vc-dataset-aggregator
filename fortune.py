from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
from dateutil import parser
import time
import urllib.request

BASE_URL = "http://fortune.com/"
TRAILING_SLASH = "/"
HYPHEN = "-"
TERM_SHEET = "term-sheet-"
BLACKLIST_DAYS = set(["Saturday","Sunday"])

def scrapeFromFortune():
    urls = generateURLs()
    for url in urls :
        time.sleep( 5 )
        backupURL = urls[url]
        processURL( url, backupURL )

def generateURLs():
    #d1 = date(2011,3, 11)  # start date
    d1 = date(2011,4, 12)  # start date
    d2 = date.today()
    delta = d2 - d1         # timedelta
    urls = {}
    for i in range(delta.days + 1):
        currentDate = d1 + timedelta(days=i)
        currentDateString = currentDate.strftime('%Y-%m-%d')
        day = parser.parse(currentDateString).strftime("%A")
        if day in BLACKLIST_DAYS :
            continue
        month = parser.parse(currentDateString).strftime("%B")
        dateParts = currentDateString.split(HYPHEN)
        backupDate = None
        if currentDate.day == 1 :
            backupDate = currentDate
        else:
            backupDate = currentDate - timedelta(days=1)
        backupDateString = backupDate.strftime('%Y-%m-%d')
        backupDateParts = backupDateString.split(HYPHEN)

        base = BASE_URL + dateParts[0] + TRAILING_SLASH + dateParts[1] + TRAILING_SLASH + dateParts[2] + TRAILING_SLASH + TERM_SHEET + day.lower() + HYPHEN + month.lower() + HYPHEN
        url =  base + dateParts[2].lstrip("0") + TRAILING_SLASH
        backupURL =  base + backupDateParts[2].lstrip("0") + TRAILING_SLASH
        urls[url] = backupURL
    return urls

def processURL(url, backupURL):
    print ( "URL = ", url )
    try:
        page = urlopen(url)
        soup = bs(page.read(), "lxml")
        h2s = soup.find_all('h2')
        for h2 in h2s:
            print(h2.string)
    except urllib.error.HTTPError as err:
        print( "Error encountered - ", err, url)
        if backupURL != None:
            print( "Will attempt to try backup URL = " + backupURL)
            processURL(backupURL,None)

################################# INVOKING SCRAPER ############################

scrapeFromFortune()

###############################################################################
