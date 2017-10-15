from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
from dateutil import parser
import time
import urllib.request
from pprint import pprint
import csv
from fortune_nlp import processSentence

BASE_URL = "http://fortune.com/"
TRAILING_SLASH = "/"
HYPHEN = "-"
TERM_SHEET = "term-sheet-"
BLACKLIST_DAYS = set(["Saturday","Sunday"])
CSV_FILE = "./assets/fortune.csv"
MULTIPLE_SEPARATOR = ":"

def scrapeFromFortune(csvfile):
    urls = generateURLs()
    for url in urls :
        time.sleep( 1 )
        backupURL = urls[url]
        processURL( csvfile, url, backupURL )

def generateURLs():
    d1 = date(2011,2, 8)  # start date
    d2 = date.today()
    delta = d2 - d1       # timedelta
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

def processURL(csvfile, url, backupURL):
    print ( "URL = ", url )
    try:
        page = urlopen(url)
        soup = bs(page.read(), "lxml")
        result = parseHTML( soup )
        processResult( csvfile, url, result )
    except urllib.error.HTTPError as err:
        print( "Error encountered - ", err, url)
        if backupURL != None:
            print( "Will attempt to try backup URL = " + backupURL)
            processURL(csvfile, backupURL,None)

def parseHTML( soup ):
    sectionResult = {}
    sections = soup.find_all('div', {'class': '_9MDA9q9L'})
    sectionNum = 0
    for section in sections:
        sectionKey = "section_" + str(sectionNum)
        sectionNum = sectionNum+1
        contents = section.contents
        contentNum = 0
        contentResult = {}
        for content in contents :
            contentRecord = []
            contentNum = contentNum+1
            isHeader = content.h2 != None
            isAnchor = content.a != None
            link = None
            if isAnchor :
                link = content.a.get('href');
            contentRecord.insert( 0, content.text )
            contentRecord.insert( 1, isHeader )
            contentRecord.insert( 2, isAnchor )
            contentRecord.insert( 3, link )
            contentKey = "content_" + str(contentNum)
            contentResult[contentKey] = contentRecord
        sectionResult[sectionKey] = contentResult
    return sectionResult

def processResult(csvfile, url,result):
    urlParts = url.split(TRAILING_SLASH)
    dayParts = urlParts[-2].split(HYPHEN)
    year = urlParts[3]
    month = urlParts[4]
    date = urlParts[5]
    day = dayParts[2]
    fullDate = str(month) + TRAILING_SLASH + str(date) + TRAILING_SLASH + str(year)
    source = "Fortune"
    parseResult(result,csvfile, source,month,date,year,day,fullDate)

def parseResult( result,csvfile, source,month,date,year,day,fullDate ):
    dealType = None
    for section in result :
        contentMap = result[section]
        count = 0
        dealType = None
        for contentKey in contentMap :
            content = contentMap[contentKey]
            if count == 0 :
                dealType = content[0]
                count = count + 1
                continue
            else :
                text = content[0]
                if text:
                    if( dealType == "VENTURE DEALS"):
                        fundingRound, funding, firms, locations, company = parseDescription(dealType, text)
                        companyLocation = MULTIPLE_SEPARATOR.join( locations );
                        investors = MULTIPLE_SEPARATOR.join( firms )
                        moneyRaised  = MULTIPLE_SEPARATOR.join( funding )
                        links = content[3]
                        leadInvestor = ""
                        writeToFile( csvfile, source,month,date,year,day,fullDate,company, companyLocation, dealType, fundingRound, moneyRaised, investors, leadInvestor, links )

def parseDescription( dealType, description ):
    if '•' in description:
        description = description[2:-1]
        return processSentence( description )
    return [''] * 5

def writeDescription( fileName, description) :
    with open(fileName, "a+", newline='') as fortune:
        wr = csv.writer(fortune, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        wr.writerow([description])

def writeToFile( csvfile, source,month,date,year,day,fullDate,company, companyLocation, dealType, fundingRound, moneyRaised, investors, leadInvestor, links ):
    print (source,month,date,year,day,fullDate,company, companyLocation, dealType, fundingRound, moneyRaised, investors, leadInvestor, links )
    with open(csvfile, "a+", newline='') as fortune:
        wr = csv.writer(fortune, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        wr.writerow([source,month,date,year,day,fullDate,company, companyLocation, dealType, fundingRound, moneyRaised, investors, leadInvestor, links ])

################################# INVOKING SCRAPER ############################

scrapeFromFortune(CSV_FILE)

###############################################################################
