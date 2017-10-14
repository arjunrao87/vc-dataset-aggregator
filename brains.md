# Format of saved datasets

1. CSV

```
source,mm,dd,yyyy,weekday,date,company,company-location,deal-type,funding-round,money-raised,investors,lead-investor,additional-links
```
eg.
```
Fortune,09,26,2017,tuesday,09-26-2017,Accelo,San Francisco,Venture,Series A,$9 million,Level Equity:Fathom Capital:Blackbird Ventures,Level Equity,,
```

## Fortune

### Time duration ( > 1500 days )

1. Term sheet started 03/01/2011 - Present

Start URL = http://fortune.com/2011/03/01/term-sheet-tuesday-march-1/

Sample present URL = http://fortune.com/2017/09/27/term-sheet-tuesday-september-26/

### Type of data

### Script

#### URL construction
```
>>> from dateutil import parser
>>> parser.parse('January 11, 2010').strftime("%a")
'Mon'
>>> parser.parse('January 11, 2010').strftime("%A")
'Monday'
>>> parser.parse('December 15, 2014').strftime("%A")
'Monday'
>>>
```
