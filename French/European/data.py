import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024_European_Parliament_election_in_France"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')



headers = ['1','Date','2','3','4','PCF','LFI','5','PS','EELV','6','7','8','EAC','9','10','PA','ENS','11','12','13','LR','14','15','16','RN','REC','17','18']
parties = ['PCF','LFI','PS','EELV','EAC','PA','ENS','LR','RN','REC']
drop = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
e = {}
for i in range(1):
  e[i]=pd.DataFrame(df[-2])
  e[i].columns = headers
  e[i]=e[i].drop(drop, axis=1)
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date2'] = [x for x in e[i]['Date2'].astype(str)]
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  e[i] = e[i][e[i]['RN'] != e[i]['ENS']]
  for z in parties: # replace any non-numeric values with NaN
    # e[i][z] = e[i][z].str.strip('%')
    e[i][z] = [p.sub('', x) for x in e[i][z].astype(str)]
    e[i][z] = [x.replace('-',str(np.NaN)) for x in e[i][z]]
    e[i][z] = [x.replace('—',str(np.NaN)) for x in e[i][z]]
    e[i][z] = [x.replace('–',str(np.NaN)) for x in e[i][z]]
    e[i][z] = [x.replace('<','') for x in e[i][z]]
    e[i].replace(r'^\s*$', str(np.NaN), regex=True)
  for z in parties: # replace any non-numeric values with NaN
    e[i][z] = pd.to_numeric(e[i][z], errors='coerce')
    e[i][z] = e[i][z].astype('float')

E = pd.concat(e.values(), ignore_index=True)

E = E[E.PS<19]
E = E[E.LFI!=12]

E.to_csv('French/European/poll.csv', index=False)
