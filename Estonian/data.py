import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Estonian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','Ref','EKRE','Kesk','E200','SDE','Isamaa','Parempoolsed']
parties = ['Ref','EKRE','Kesk','E200','SDE','Isamaa','Parempoolsed']
d = {}
for i in range(3):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Others", "Lead", "Gov.", "Opp.", 'EÜVP','Koos','EER'], axis=1)
  if i != 2:
    d[i]=d[i].drop(['ERK'], axis=1)
  d[i].columns = headers
  for z in headers:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Isamaa'] != d[i]['Parempoolsed']]
for i in range(2):
  d[i].drop(d[i].index[[-1,-2]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[-1]],inplace=True)

D.to_csv('Estonian/poll.csv', index=False)
