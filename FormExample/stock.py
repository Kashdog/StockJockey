import sys
import time
import requests

apiEndpoint = "https://query1.finance.yahoo.com/v7/finance/quote"
fields = [
    'symbol',
    'regularMarketVolume',
    'regularMarketPrice',
    'regularMarketDayHigh',
    'regularMarketDayLow',
    'regularMarketTime',
    'regularMarketChangePercent']
fields = ','.join(fields)
symbols ='AAPL'
payload = {
    'lang': 'en-US',
    'region': 'US',
    'corsDomain': 'finance.yahoo.com',
    'fields': fields,
    'symbols': symbols}
r = requests.get(apiEndpoint, params=payload)
print(r.json())
for i in r.json()['quoteResponse']['result']:
    print(i['regularMarketPrice'])
    if 'regularMarketPrice' in i:
        a = []
        a.append(i['symbol'])
        a.append(i['regularMarketPrice'])
        a.append(time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(i['regularMarketTime'])))
        a.append(i['regularMarketChangePercent'])
        a.append(i['regularMarketVolume'])
        a.append("{0:.2f} - {1:.2f}".format(
            i['regularMarketDayLow'], i['regularMarketDayHigh']))
        print(",".join([str(e) for e in a]))

import re
import sys
import time
import datetime
import requests

def get_cookie_value(r):
    return {'B': r.cookies['B']}

def get_page_data(symbol):
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
    r = requests.get(url)
    cookie = get_cookie_value(r)
    lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
    return cookie, lines.split('\n')

def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")

def split_crumb_store(v):
    return v.split(':')[2].strip('"')

def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb

def get_data(symbol, start_date, end_date, cookie, crumb):
    filename = '%s.csv' % (symbol)
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie)
    with open (filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)
    import csv
    with open('%s.csv' % (symbol), 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        stockarray = []
        for row in spamreader:
            stockarray.append(row)
        print(stockarray[len(stockarray)-1][0].split(",")[1])

def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())

def download_quotes(symbol):
    start_date = 0
    end_date = get_now_epoch()
    cookie, crumb = get_cookie_crumb(symbol)
    get_data(symbol, start_date, end_date, cookie, crumb)

symbol = 'AAPL'
#print("--------------------------------------------------")
#print("Downloading %s to %s.csv" % (symbol, symbol))
download_quotes(symbol)
#print("--------------------------------------------------")