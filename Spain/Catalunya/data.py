import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re
from io import StringIO


wikiurl="https://es.wikipedia.org/wiki/Elecciones_al_Parlamento_de_Catalu%C3%B1a_de_2024"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['1','Date','2','3','PSC','ERC','Junts','VOX','ECP','CUP','Cs','PP','4','5','6','AC','7']
parties = ['PSC','ERC','Junts','VOX','ECP','CUP','Cs','PP','AC']
drops = ['1','2','3','4','5','6','7']

headers = ['1','Date','2','3','PSC','ERC','Junts','VOX','ECP','CUP','Cs','PP','AC','4']
parties = ['PSC','ERC','Junts','VOX','ECP','CUP','Cs','PP','AC']
drops = ['1','2','3','4']

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[3])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 May 2023']
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['PSC'] != d[i]['Cs']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str()) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]

D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)

D.to_csv('Spain/Catalunya/poll.csv', index=False)





d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[3])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 May 2023']
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['PSC'] != d[i]['Cs']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[1]
    d[i][z] = [x.split('/')[1] if len(x.split('/')) > 1 else x for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str()) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]

D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
D[parties] = D[parties].astype(float)
D.drop(D.index[[-1,-3]],inplace=True)

D.to_csv('Spain/Catalunya/seats.csv', index=False)
