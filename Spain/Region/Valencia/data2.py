import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Next_Valencian_regional_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )


headers = ['1','Date','2','3','PP','PSOE','Compromís','VOX','Podemos','4','SALF','5']
parties = ['PP','PSOE','Compromís','VOX','Podemos','SALF']
drops = ['1','2','3','4','5']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-6])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]=d[i][~d[i].Date.str.contains("9 Jun 2024")]
  d[i]=d[i][~d[i].Date.str.contains("23 Jul 2023")]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[1]
    d[i][z] = d[i][z].str.split('/').str[0]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['PP'])


D = pd.concat(d.values(), ignore_index=True)

# D['Compromís']=np.where(pd.isna(D['Compromís'])==True,D['Sumar'],D['Compromís'])
# D['Sumar']=np.where(D['Compromís']==D['Sumar'],np.nan,D['Sumar'])
# D=D.drop(['Sumar'], axis=1)


D=D[['Date','Podemos','Compromís','PSOE','PP','VOX','SALF']]

D.to_csv('Spain/Region/Valencia/poll2.csv', index=False)
