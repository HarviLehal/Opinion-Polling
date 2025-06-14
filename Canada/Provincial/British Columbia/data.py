import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/44th_British_Columbia_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['1','Date','2','NDP','Con','Green','OneBC','CentreBC','Others','3','4','5','6']
parties = ['NDP','Con','Green','OneBC','CentreBC','Others']
drops = ['1','2','3','4','5','6']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split(' ').str[0]
  d[i]['Date3'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date3.fillna(d[i]['Date'].str.split(' ').str[1], inplace=True)
  d[i]['Date3'] = d[i]['Date3'].str.split(',').str[0]
  d[i]['Date4'] = d[i]['Date'].str.split(' ').str[-1]
  d[i]['Date'] = d[i]['Date3']+ ' ' +d[i]['Date2'] + ' ' +d[i]['Date4']
  d[i] = d[i].drop(['Date2','Date3','Date4'], axis=1)
  d[i].loc[len(d[i].index)-1,['Date']] = '19 Oct 2024'
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['NDP'])
  # d[i].drop(d[i].index[[-1,-2,-4]],inplace=True)
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.strip('%')
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['NDP'])
  
  

# d[0]['Date'].replace({pd.NaT: "0 days"}, inplace=True)



D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [x.replace('–',str(np.nan)) for x in D[z]]
  D[z] = [x.replace('—',str(np.nan)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
  
D = D.dropna(subset=['Date'])

D.to_csv('Canada/Provincial/British Columbia/poll.csv', index=False)

# split_date = '21 September 2024'
# split_date=dateparser.parse(split_date)
# z=D.tail(1)
# D=D[(pd.to_datetime(D["Date"]) > split_date)]
# D = pd.concat([D,z], ignore_index=True)
# # D=D.drop(['BCU'], axis=1)
# 
# D.to_csv('Canada/Provincial/British Columbia/poll2.csv', index=False)
