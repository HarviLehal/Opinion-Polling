import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_45th_Canadian_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['1','Date','2','CPC','LPC','NDP','BQ','PPC','GPC','3','4','5','6','7']
parties = ['CPC','LPC','NDP','BQ','PPC','GPC']
drops = ['1','2','3','4','5','6','7']
d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  # d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  # d[i]['Date'] = d[i]['Date2']
  # d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['CPC'] != d[i]['BQ']]
  # d[i].drop(d[i].index[[-1,-2,-4]],inplace=True)
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['CPC'])
  
D = pd.concat(d.values(), ignore_index=True)
D.to_csv('Canada/Federal/poll.csv', index=False)

split_date = '23 March 2025'
split_date=dateparser.parse(split_date)
z=D.tail(1)
D=D[(pd.to_datetime(D["Date"]) > split_date)]
D = pd.concat([D,z], ignore_index=True)

D.to_csv('Canada/Federal/poll2.csv', index=False)
