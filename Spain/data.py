import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Spanish_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','drop3','PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','drop4','drop5','drop6','Podemos','SALF','drop7']
parties = ['PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','Podemos','SALF']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7']
d = {}
for i in range(3):
  d[i]=pd.DataFrame(df[i])
  if i == 2:
    headers = ['drop1','Date','drop2','drop3','PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','drop4','drop5','drop6','Podemos','drop7']
    parties = ['PP','PSOE','VOX','Sumar','ERC','JxCat','EHB','PNV','Podemos']
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['PSOE'] != d[i]['EHB']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z].astype(str)]


D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.nan, regex=True)
parties = ['PP','PSOE','VOX','Sumar','Podemos','ERC','JxCat','EHB','PNV','SALF']
D[parties] = D[parties].astype(float)
D = D[['Date','PSOE','PP','Sumar','Podemos','VOX','ERC','JxCat','PNV','EHB','SALF']]
D.drop(D.index[[-1,-3]],inplace=True)


D.to_csv('Spain/poll.csv', index=False)

Left = ['Sumar','PSOE','PNV','EHB','ERC','JxCat','Podemos']
Right = ['PP','VOX','SALF']
D['Govt (PSOE + Sumar + EHB + ERC + PNV + JxCat + Podemos)'] = D[Left].sum(axis=1)
D['Right (PP + VOX + SALF)'] = D[Right].sum(axis=1)
D = D.drop(Left + Right, axis=1)
# D = D.drop('SALF', axis=1)


D=D.drop(D[D['Govt (PSOE + Sumar + EHB + ERC + PNV + JxCat + Podemos)'] < 20].index)
D=D.drop(D[D['Right (PP + VOX + SALF)'] < 20].index)

D.to_csv('Spain/poll2.csv', index=False)
