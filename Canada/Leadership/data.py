import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_46th_Canadian_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i-3])
  headers = ['1','Date','2','Carney','Poilievre','Blanchet','Davies','May','Bernier','3','4','5']
  parties = ['Carney','Poilievre','Blanchet','Davies','May','Bernier']
  drops = ['1','2','3','4','5']
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  # d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  # d[i]['Date'] = d[i]['Date2']
  # d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Poilievre'] != d[i]['Blanchet']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  
D = pd.concat(d.values(), ignore_index=True)
D = D.dropna(subset=['Carney'])
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)*100
D = D.drop(["total"], axis=1)
D.to_csv('Canada/Leadership/poll.csv', index=False)
