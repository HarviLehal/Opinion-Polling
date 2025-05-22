import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2025_Polish_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z 0-9]+\]')

headers = ['1','Date','2','Nawrocki','Trzaskowski','Hołownia','Biejat','Zandberg','Mentzen','Braun','Jakubiak','Stanowski','3','4','5','6','7','8','9']
parties = ['Nawrocki','Trzaskowski','Hołownia','Biejat','Zandberg','Mentzen','Jakubiak','Stanowski']
drops = ['1','2','3','4','5','6','7','8','9']
d = {}
for i in range(1):
  # i=j+1
  d[i]=pd.DataFrame(df[1])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z]]#
  d[i]['Date'] = [p.sub('', x) for x in d[i]['Date'].astype(str)]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = pd.to_numeric(D[z], errors='coerce')

D=D.dropna(subset=['Date'])
D=D.dropna(subset=['Trzaskowski'])


c={}
c[0] = D[:1]
c[1] = D[1:]
c[1] = c[1][(pd.to_datetime(c[1]["Date"])<dateparser.parse("17 May 2025"))]
D = pd.concat(c.values(), ignore_index=True)

D.to_csv('Polish/President/poll_new.csv', index=False)








headers = ['1','Date','2','Nawrocki','Trzaskowski','3','4','5']
parties = ['Nawrocki','Trzaskowski']
drops = ['1','2','3','4','5']
d = {}
for i in range(1):
  # i=j+1
  d[i]=pd.DataFrame(df[3])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z]]#
  d[i]['Date'] = [p.sub('', x) for x in d[i]['Date'].astype(str)]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Trzaskowski'])
D['total']=D[parties].sum(axis=1)
D[parties]=D[parties].div(D['total'], axis=0)
D = D.drop(['total'], axis=1)
D.to_csv('Polish/President/poll2.csv', index=False)
