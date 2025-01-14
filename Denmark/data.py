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

headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','Å','O','3','4','5','6','7','8']
parties = ['A','V','M','F','Æ','I','C','Ø','B','Å','O']
drop = ['1','2','3','4','5','6','7','8']

d = {}
for i in range(4):
  if i == 0:
    pass
  elif i ==1:
    headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','D','Å','O','3','4','5','6','7','8']
    parties = ['A','V','M','F','Æ','I','C','Ø','B','D','Å','O']
    drop = ['1','2','3','4','5','6','7','8']
  else:
    headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','D','Å','O','3','4','5','6','7','8','9']
    drop = ['1','2','3','4','5','6','7','8','9']
  d[i]=pd.DataFrame(df[i+1])
  d[i].columns = headers
  d[i]=d[i].drop(drop, axis=1)
  d[i] = d[i][d[i]['Date'] != '2024 EU election result']
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  # d[i] =  d[i].dropna(subset=['Date'])
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  # d[i] =  d[i].dropna(subset=['Date'])
  # d[i] = d[i][d[i]['A'] != d[i]['Å']]
  # d[i].drop(d[i].index[[-2]],inplace=True)
  for z in parties:
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] =  d[i].dropna(subset=['A'])
  d[i]=d[i].reset_index(drop=True)
  if i != 3:
    d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)

D.loc[len(D.index)-1,['Date']] = '2022-11-01'
D.Date = D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# D[parties] = D[parties].astype(float)

print(D)

D = D[['Date','A','V','M','F','Æ','I','C','Ø','B','D','Å','O']]


D.to_csv('Denmark/poll.csv', index=False)



headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','Å','O','3','4','5','6']
parties = ['A','V','M','F','Æ','I','C','Ø','B','Å','O']
drop = ['1','2','3','4','5','6']

d = {}
for i in range(4):
  if i ==2:
    headers = ['1','Date','2','A','V','M','F','Æ','I','C','Ø','B','D','Å','O','3','4','5','6','7']
    parties = ['A','V','M','F','Æ','I','C','Ø','B','D','Å','O']
    drop = ['1','2','3','4','5','6','7']
  d[i]=pd.DataFrame(df[i+6])
  d[i].columns = headers
  d[i]=d[i].drop(drop, axis=1)
  d[i] = d[i][d[i]['Date'] != '2024 EU election result']
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  # d[i] =  d[i].dropna(subset=['Date'])
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  # d[i] =  d[i].dropna(subset=['Date'])
  # d[i] = d[i][d[i]['A'] != d[i]['Å']]
  # d[i].drop(d[i].index[[-2]],inplace=True)
  for z in parties:
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] =  d[i].dropna(subset=['A'])
  d[i]=d[i].reset_index(drop=True)
  if i != 3:
    d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.loc[len(D.index)-1,['Date']] = '2022-11-01'
D.Date = D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D[parties] = D[parties].astype(float)

print(D)

D = D[['Date','A','V','M','F','Æ','I','C','Ø','B','D','Å','O']]

D.to_csv('Denmark/poll2.csv', index=False)


parties= ['A','V','M','F','Æ','I','C','Ø','B','D','Å','O']

govt = ['A','V','M']

D[parties] = D[parties].astype(float)
D['Government'] = D[govt].sum(axis=1)
D['Opposition'] = 175- D['Government']

D = D.drop(parties, axis=1)

D.to_csv('Denmark/poll_govt2.csv', index=False)




D = pd.concat(d.values(), ignore_index=True)
D.loc[len(D.index)-1,['Date']] = '2022-11-01'
D.Date = D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D[parties] = D[parties].astype(float)

print(D)

D = D[['Date','A','V','M','F','Æ','I','C','Ø','B','D','Å','O']]

parties= ['A','V','M','F','Æ','I','C','Ø','B','D','Å','O']

govt = ['A','B','F','Ø','Å']
opp = ['V','Æ','I','C','D','O']

D[parties] = D[parties].astype(float)
D['Red'] = D[govt].sum(axis=1)
D['Blue'] = D[opp].sum(axis=1)

D = D.drop(govt, axis=1)
D = D.drop(opp, axis=1)

D = D[['Date','Red','M','Blue']]
D.to_csv('Denmark/poll_bloc.csv', index=False)
