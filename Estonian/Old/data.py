import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Estonian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','R','K','EKRE','I','SDE','E200','ER']
parties = ['R','K','EKRE','I','SDE','E200','ER']
d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Others", "Lead", "Gov.", "Opp.", "Parem"], axis=1)
  d[i].columns = headers
  for z in headers:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]

  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['R'] != d[i]['SDE']]


headers = ['Date','R','K','EKRE','I','SDE','E200','ER']
parties = ['R','K','EKRE','I','SDE','E200','ER']
for i in range(2):
  d[i+2]=pd.DataFrame(df[i+2])
  d[i+2]=d[i+2].drop(["Polling firm", "Sample size", "Others", "Lead", "Gov.", "Opp."], axis=1)
  d[i+2].columns = headers
  for z in headers:
      d[i+2][z] = [p.sub('', x) for x in d[i+2][z].astype(str)]
  d[i+2]['Date2'] = d[i+2]['Date'].str.split('–').str[1]
  d[i+2].Date2.fillna(d[i+2]['Date'].str.split('-').str[1], inplace=True)
  d[i+2].Date2.fillna(d[i+2].Date, inplace=True)
  d[i+2]['Date2'] = [x+ str(2022-i) for x in d[i+2]['Date2'].astype(str)]
  d[i+2]['Date'] = d[i+2]['Date2']
  d[i+2] = d[i+2].drop(['Date2'], axis=1)
  d[i+2].Date=d[i+2].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i+2] = d[i+2][d[i+2]['R'] != d[i+2]['SDE']]

d[4]=pd.DataFrame(df[4])
d[4]=d[4].drop(["Polling firm", "Sample size", "Others", "Lead", "Gov.", "Opp.","TULE"], axis=1)
d[4].columns = headers
for z in headers:
   d[4][z] = [p.sub('', x) for x in d[4][z].astype(str)]
d[4]['Date2'] = d[4]['Date'].str.split('–').str[1]
d[4].Date2.fillna(d[4]['Date'].str.split('-').str[1], inplace=True)
d[4].Date2.fillna(d[4].Date, inplace=True)
d[4]['Date2'] = [x+ str(2020) for x in d[4]['Date2'].astype(str)]
d[4]['Date'] = d[4]['Date2']
d[4] = d[4].drop(['Date2'], axis=1)
d[4].Date=d[4].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
d[4] = d[4][d[4]['R'] != d[4]['SDE']]
  


for i in range(2):
  d[i+5]=pd.DataFrame(df[i+5])
  d[i+5]=d[i+5].drop(["Polling firm", "Sample size", "Others", "Lead", "Gov.", "Opp.","EVA"], axis=1)
  d[i+5].columns = headers
  for z in headers:
    d[i+5][z] = [p.sub('', x) for x in d[i+5][z].astype(str)]

  d[i+5]['Date2'] = d[i+5]['Date'].str.split('–').str[1]
  d[i+5].Date2.fillna(d[i+5]['Date'].str.split('-').str[1], inplace=True)
  d[i+5].Date2.fillna(d[i+5].Date, inplace=True)
  d[i+5]['Date2'] = [x+ str(2020-i) for x in d[i+5]['Date2'].astype(str)]
  d[i+5]['Date'] = d[i+5]['Date2']
  d[i+5] = d[i+5].drop(['Date2'], axis=1)
  d[i+5].Date=d[i+5].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i+5] = d[i+5][d[i+5]['R'] != d[i+5]['SDE']]


D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[-1,1]],inplace=True)

D.to_csv('Estonian/poll.csv', index=False)
