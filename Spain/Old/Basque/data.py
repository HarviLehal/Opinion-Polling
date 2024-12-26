import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024_Basque_regional_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['1','Date','2','3','PNV','EHB','PSE','EP','PPCS','Vox','PP','4','Sumar','5']
parties = ['PNV','EHB','PSE','EP','PPCS','Vox','PP','Sumar']
drops = ['1','2','3','4','5']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[4])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '23 Jul 2023']
  d[i] = d[i][d[i]['Date'] != '28 May 2023']
  d[i].loc[3,['Date']] = '20 Apr 2024'
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['PNV'] != d[i]['PSE']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–','') for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z].astype(str)]
  


D = pd.concat(d.values(), ignore_index=True)

D = D.replace(r'^\s*$', np.nan, regex=True)

# parties = ['PNV','EHB','PSE','EP','Vox','PP','Sumar']
D[parties] = D[parties].astype(float)
D.PP.fillna(D.PPCS, inplace=True)
D=D.drop(['PPCS'], axis=1)

D=D.dropna(subset=['PNV'])

# D.drop(D.index[[0]],inplace=True)
# new_row = pd.DataFrame({'Date': '18 Feb 2024','PP':47.35,'BNG':31.58,'PSOE':14.04,'Podemos':0.26, 'VOX':2.19, 'CS':np.nan, 'Sumar':1.90,'DO':1.03}, index=[0])
# D = pd.concat([new_row,D]).reset_index(drop=True)
# D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D.to_csv('Spain/Basque/poll.csv', index=False)
