import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2025_Norwegian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['1','Date','2','3','R','SV','MDG','Ap','Sp','V','KrF','H','FrP','INP','4','5']
parties = ['R','SV','MDG','Ap','Sp','V','KrF','H','FrP','INP']
drops = ['1','2','3','4','5']
d = {}

for i in range(3):
  d[i]=pd.DataFrame(df[i+1])
  if i == 0:
    d[i]=d[i].drop(["Blocs"],axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['KrF'] != d[i]['H']]
  if i == 0:
    for z in parties:
      d[i][z] = d[i][z].str.split(' ').str[0]


headers = ['1','Date','2','3','R','SV','MDG','Ap','Sp','V','KrF','H','FrP','4','5']
parties = ['R','SV','MDG','Ap','Sp','V','KrF','H','FrP']
drops = ['1','2','3','4','5']

for j in range(2):
  i = j+3
  d[i]=pd.DataFrame(df[i+1])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['KrF'] != d[i]['H']]

for i in range(4):
  d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.to_csv('Norwegian/poll.csv', index=False)


parties = ['R','SV','MDG','Ap','Sp','V','KrF','H','FrP','INP']
red = ['Ap','R','Sp','SV','MDG']
blue = ['FrP','H','KrF','V']

for z in parties:
  D[z] = pd.to_numeric(D[z], errors='coerce')
  # D[z] = D[z].apply(lambda x: x if x > 4 else 0)

D['Red'] = D[red].sum(axis=1)
D['Blue'] = D[blue].sum(axis=1)

D = D.drop(parties, axis=1)
parties=['Red','Blue']
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)
D = D.drop(["total"], axis=1)
D = D[['Date','Red','Blue']]
D.to_csv('Norwegian/poll2.csv', index=False)

