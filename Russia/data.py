import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_Russian_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','UR','CPRF','LDPR','SRZP','NP']
parties = ['UR','CPRF','LDPR','SRZP','NP']
d = {}
for i in range(4):
  # i=j+1
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Polling firm", "Sample size"], axis=1)
  d[i] = d[i].iloc[:, :6]
  d[i].columns = headers
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  if i == 0:
    d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  else:
    d[i]['Date2'] = [x+ str(2024-i+1) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  if i != 3:
    d[i].drop(d[i].index[[-1]],inplace=True)
d[3].loc[len(d[3].index)-1,['Date']] = '19 Sep 2021'
D = pd.concat(d.values(), ignore_index=True)
D=D.dropna(subset=['UR'])


D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)*100
D = D.drop(["total"], axis=1)

D.to_csv('Russia/poll.csv', index=False)
