import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://tr.wikipedia.org/w/index.php?title=Bir_sonraki_T%C3%BCrkiye_cumhurba%C5%9Fkanl%C4%B1%C4%9F%C4%B1_se%C3%A7imi_i%C3%A7in_yap%C4%B1lan_anketler&stable=0"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')
p = re.compile(r'\[[a-z 0-9]+\]'  )

d = {}
for i in range(2):
  print(i)
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  heads = [p.sub('', x) for x in heads]
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  d[i] = d[i].drop(d[i].columns[[1, 2,4,5,-1]],axis = 1)
  # parties = d[i].columns[1:].remove_unused_levels().levels[0]
  # if i==2:
  parties = d[i].columns[1:]
  heads = parties.insert(0,'Date')
  d[i].columns = heads
  d[i].rename(columns={d[i].columns[0]: 'Date'}, inplace=True)
  d[i].rename(columns={'Demirtaş DEM[a 1]': 'Demirtaş DEM'}, inplace=True)
  d[i]['Date2'] = d[i]['Date'].str.split('-').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+' '+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  for z in parties:
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=[d[i].columns[1]])
# d[2] = d[2].drop(['MP'], axis=1)
for i in range(2):
  d[i]=d[i].reset_index(drop=True)
# d[0].loc[len(d[0].index)-11,['Date']] = '29 March 2025'

D = pd.concat(d.values(), ignore_index=True)

CHP = [D.columns[2],D.columns[3],D.columns[4]]
dig = [D.columns[7],D.columns[8],D.columns[9],D.columns[10]]

D['Other'] = D[dig].sum(axis=1)
D['CHP'] = np.where(D[CHP[0]]==D[CHP[1]],D[CHP[0]],D[CHP].sum(axis=1))

D = D.drop(CHP+dig,axis=1)

heads = D.columns

D=D[[heads[0],heads[1],heads[-1],heads[2],heads[3],heads[-2]]]

new_row = pd.DataFrame({'Date': '14 May 2023', heads[1]:49.24 , heads[-1]:45.07 , heads[-2]:5.69}, index=[0])
D = pd.concat([D,new_row]).reset_index(drop=True)

D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, languages=['tr'], settings={'PREFER_DAY_OF_MONTH': 'first'}))
# D['Date'] = D['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
D['Date'] = D['Date'].apply(lambda x: x.date())
# D['Date'] = D['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

D.to_csv('Turkish/President/poll.csv', index=False)

