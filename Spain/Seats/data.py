import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re
import math


wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Spanish_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )


headers = ['1','Date','2','3','PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','BNG','CCa','UPN','Podemos','SALF','4']
parties = ['PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','BNG','CCa','UPN','Podemos','SALF']
drops = ['1','2','3','4']
d = {}
for i in range(3):
  d[i]=pd.DataFrame(df[i])
  if i == 2:
    headers = ['1','Date','2','3','PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','BNG','CCa','UPN','Podemos','4']
    parties = ['PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','BNG','CCa','UPN','Podemos']
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]=d[i][~d[i].Date.str.contains("9 Jun 2024")]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[1]
    d[i][z] = d[i][z].str.split('/').str[0]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i].dropna(subset=['PSOE'])

D = pd.concat(d.values(), ignore_index=True)
parties = ['PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','BNG','CCa','UPN','Podemos','SALF']
D['total']=D[parties].sum(axis=1)
D['total']=np.where(D['total']<325,np.nan,D['total'])
D=D.dropna(subset=['total'])
D=D.drop(['total'], axis=1)

D.to_csv('Spain/Seats/poll2.csv', index=False)


opp = ['PP','VOX','UPN','SALF']
gov = ['PSOE','Sumar','ERC','JxCat','EHB','PNV','BNG','CCa','Podemos']
D['Government']=D[gov].sum(axis=1)
D['Opposition']=D[opp].sum(axis=1)
D=D.drop(gov+opp, axis=1)

D.to_csv('Spain/Seats/poll.csv', index=False)

