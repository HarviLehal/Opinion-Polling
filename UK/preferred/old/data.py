import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_2024_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers = ['Date','1','2','3','Truss','Starmer','4','5','6']
parties = ['Truss','Starmer']
drops = ['1','2','3','4','5','6']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[32])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ " "+ str(2022-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.strip('%')
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  
  d[i] = d[i].dropna(subset=['Starmer'])


D = pd.concat(d.values(), ignore_index=True)
parties = ['Truss','Starmer']
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)
D = D.drop(["total"], axis=1)

D = D.loc[~D.index.isin(D[D["Starmer"]>0.9999].index)]

split_date = '5 September 2022'
split_date=dateparser.parse(split_date)
D=D[(pd.to_datetime(D["Date"]) > split_date)]


D.to_csv('UK/preferred/old/poll2.csv', index=False)




headers = ['Date','1','2','3','Johnson','Starmer','4','5','6','7']
parties = ['Johnson','Starmer']
drops = ['1','2','3','4','5','6','7']
d = {}
for i in range(3):
  d[i]=pd.DataFrame(df[33+i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ " "+ str(2022-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.strip('%')
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')

  d[i] = d[i].dropna(subset=['Starmer'])


D = pd.concat(d.values(), ignore_index=True)
parties = ['Johnson','Starmer']
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)
D = D.drop(["total"], axis=1)

D = D.loc[~D.index.isin(D[D["Starmer"]>0.9999].index)]


D.to_csv('UK/preferred/old/poll3.csv', index=False)






headers = ['Date','1','2','3','Starmer','Sunak','4','5']
parties = ['Starmer','Sunak']
drops = ['1','2','3','4','5']
d = {}
for i in range(5):
  d[i]=pd.DataFrame(df[27+i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ " "+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.strip('%')
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  
  d[i] = d[i].dropna(subset=['Starmer'])


D = pd.concat(d.values(), ignore_index=True)
parties = ['Starmer','Sunak']
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)
D = D.drop(["total"], axis=1)

D = D.loc[~D.index.isin(D[D["Starmer"]>0.9999].index)]

split_date = '20 October 2022'
split_date=dateparser.parse(split_date)
D=D[(pd.to_datetime(D["Date"]) > split_date)]



wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','1','2','Starmer','Sunak','3','4','5']
parties = ['Starmer','Sunak']
drops = ['1','2','3','4','5']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[1])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.strip('%')
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  
  d[i] = d[i].dropna(subset=['Starmer'])

E = pd.concat(d.values(), ignore_index=True)
parties = ['Starmer','Sunak']
E['total']=E[parties].sum(axis=1)
E[parties] = E[parties].div(E['total'], axis=0)
E = E.drop(["total"], axis=1)

E = E.loc[~E.index.isin(E[E["Starmer"]>0.9999].index)]

D = pd.concat([E,D], ignore_index=True)

D.to_csv('UK/preferred/old/poll.csv', index=False)
