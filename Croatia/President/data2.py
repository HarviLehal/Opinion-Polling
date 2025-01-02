import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024–25_Croatian_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers=['Date','1','Milanović','Primorac','2','3']
parties = ['Milanović','Primorac']
drops = ['1','2','3']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i+2])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['Milanović'])
  
D = pd.concat(d.values(), ignore_index=True)
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)*100
D = D.drop(["total"], axis=1)
D.to_csv('Croatia/President/poll2.csv', index=False)
