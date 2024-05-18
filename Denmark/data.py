import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Danish_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','D','Å','O','3','4','5','6','7','8','9']
parties = ['A','V','M','F','Æ','I','C','Ø','B','D','Å','O']
drop = ['1','2','3','4','5','6','7','8','9']

d = {}
for i in range(3):
  if i == 0:
    pass
  else:
    headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','D','Å','O','3','4','5','6','7','8','9','10']
    drop = ['1','2','3','4','5','6','7','8','9','10']
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drop, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['A'] != d[i]['Å']]
  d[i].drop(d[i].index[[-2]],inplace=True)
  for z in parties:
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
  if i != 2:
    d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.loc[len(D.index)-1,['Date']] = '2022-11-01'
D.Date = D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D[parties] = D[parties].astype(float)

print(D)



D.to_csv('Denmark/poll.csv', index=False)



headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','D','Å','O','3','4','5','6','7']
parties = ['A','V','M','F','Æ','I','C','Ø','B','D','Å','O']
drop = ['1','2','3','4','5','6','7']

d = {}
for i in range(3):
  if i == 0:
    pass
  else:
    headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','D','Å','O','3','4','5','6','7','8']
    drop = ['1','2','3','4','5','6','7','8']
  d[i]=pd.DataFrame(df[i+4])
  d[i].columns = headers
  d[i]=d[i].drop(drop, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['A'] != d[i]['Å']]
  d[i].drop(d[i].index[[-2]],inplace=True)
  for z in parties:
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
  if i != 2:
    d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.loc[len(D.index)-1,['Date']] = '2022-11-01'
D.Date = D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D[parties] = D[parties].astype(float)

print(D)



D.to_csv('Denmark/poll2.csv', index=False)
