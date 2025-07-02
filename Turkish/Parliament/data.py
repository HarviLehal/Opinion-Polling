import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://tr.wikipedia.org/wiki/Bir_sonraki_T%C3%BCrkiye_genel_se%C3%A7imleri_i%C3%A7in_yap%C4%B1lan_anketler"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')

d = {}
for i in range(3):
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  parties = heads[3:-2]
  d[i] = d[i].drop(d[i].columns[[1, 2,-1,-2]],axis = 1)
  d[i].rename(columns={'Tarih': 'Date'}, inplace=True)
  d[i]['Date2'] = d[i]['Date'].str.split('-').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+' '+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  for z in parties:
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['AKP'])
# d[2] = d[2].drop(['MP'], axis=1)
for i in range(3):
  d[i]=d[i].reset_index(drop=True)

# d[1].loc[len(d[1].index)-12,['Date']] = ' 1 May 2024'
# d[1].loc[len(d[1].index)-5,['Date']] = ' 1 Nis 2024'
# d[1].loc[len(d[1].index)-3,['Date']] = ' 5 Mar 2024'
# d[2].loc[len(d[2].index)-1,['Date']] = '14 May 2023'

for i in range(2):
  d[i].drop(d[i].index[[-1]],inplace=True)
d[1] = d[1][d[1]['Date'] != '31 Mart 2024']

D = pd.concat(d.values(), ignore_index=True)
# D = D.drop(D.columns[[-1]],axis = 1)


D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, languages=['tr'], settings={'PREFER_DAY_OF_MONTH': 'first'}))
# D['Date'] = D['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
D['Date'] = D['Date'].apply(lambda x: x.date())
# D['Date'] = D['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

D.to_csv('Turkish/Parliament/poll.csv', index=False)

