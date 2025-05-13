import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://es.wikipedia.org/wiki/Gobierno_de_Dina_Boluarte"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z 0-9]+\]')

headers = ['1','Date','2','Approve','Disapprove','Neither','3']
parties = ['Approve','Disapprove','Neither']
drops = ['1','2','3']
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
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x,languages=['es'], settings={'PREFER_DAY_OF_MONTH': 'first'}))


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Approve'])
D.to_csv('Peru/poll.csv', index=False)

D = D.drop(['Neither'], axis=1)
parties=['Approve','Disapprove']
D['total']=D[parties].sum(axis=1)
D[parties]=D[parties].div(D['total'], axis=0)
D = D.drop(['total'], axis=1)
D['Net Approval'] = D['Approve']-D['Disapprove']

D = D.drop(parties,axis=1)

D.to_csv('Peru/poll2.csv', index=False)
