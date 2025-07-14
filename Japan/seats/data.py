import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2025_Japanese_House_of_Councillors_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','LDP','CDP','NIK','DPP','KMT','REI','JCP','DIY','CPJ','SDP','Oth','Gov','Opp']
parties = ['LDP','CDP','NIK','DPP','KMT','REI','JCP','DIY','CPJ','SDP','Oth','Gov','Opp']
d = {}

for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i]=d[i].drop(["Analysts","Publication/ Newspapers","Gov. Majority"], axis=1)
  d[i].columns = headers
  # d[i]=d[i][~d[i].Date.str.contains("13 Oct 2024")]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  # d[i].drop([1,2],axis=0,inplace=True)#
  d[i]=d[i].reset_index(drop=True)
  for z in parties:
    d[i][z] = [x.replace('~','') for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('>','') for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('<','') for x in d[i][z].astype(str)]
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].astype(str)
    for x in range(len(d[i][z])):
      if len(d[i][z][x].split(' '))>1:
        d[i][z][x] = d[i][z][x].split(' ')[0]
      elif len(d[i][z][x].split('–'))>1:
        d[i][z][x] = d[i][z][x].split('–')[0]
      else:
        d[i][z][x] = d[i][z][x]
  for z in parties:
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')

e = {}
for i in range(1):
  e[i]=pd.DataFrame(df[-1])
  e[i]=e[i].drop(["Analysts","Publication/ Newspapers","Gov. Majority"], axis=1)
  e[i].columns = headers
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  # e[i].drop([1,2],axis=0,inplace=True)
  e[i]=e[i].reset_index(drop=True)
  for z in parties:
    e[i][z] = [x.replace('~','') for x in e[i][z].astype(str)]
    e[i][z] = [x.replace('>','') for x in e[i][z].astype(str)]
    e[i][z] = [x.replace('<','') for x in e[i][z].astype(str)]
    e[i][z] = [p.sub('', x) for x in e[i][z].astype(str)]
    e[i][z] = e[i][z].astype(str)
    for x in range(len(e[i][z])):
      if len(e[i][z][x].split(' '))>1:
        e[i][z][x] = e[i][z][x].split(' ')[0]
      elif len(e[i][z][x].split('–'))>1:
        e[i][z][x] = e[i][z][x].split('–')[1]
      else:
        e[i][z][x] = e[i][z][x]
  for z in parties:
    e[i][z] = pd.to_numeric(e[i][z], errors='coerce')


D = pd.concat(d.values(), ignore_index=True)
# split_date = '13 October 2024'
# split_date=dateparser.parse(split_date)
# D=D[(pd.to_datetime(D["Date"]) != split_date)]
E = pd.concat(e.values(), ignore_index=True)
# E=E[(pd.to_datetime(E["Date"]) != split_date)]
D = pd.concat([D,E], ignore_index=True)
D=D.drop_duplicates()




D=D.drop(['Gov','Opp'], axis=1)

D.to_csv('Japan/seats/poll.csv', index=False)

D = pd.concat(d.values(), ignore_index=True)
# D=D[(pd.to_datetime(D["Date"]) != split_date)]
E = pd.concat(e.values(), ignore_index=True)
# E=E[(pd.to_datetime(E["Date"]) != split_date)]
D = pd.concat([D,E], ignore_index=True)
D=D.drop_duplicates()
D=D.drop(['LDP','CDP','NIK','KMT','JCP','DPP','REI','DIY','SDP','CPJ','Oth'], axis=1)
D.to_csv('Japan/seats/poll2.csv', index=False)
