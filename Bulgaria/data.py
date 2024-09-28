import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/October_2024_Bulgarian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','GERB','DPS1','DPS2','PP-DB','V','BSP','ITN','Velichie','drop3','Other','drop4','drop5','drop6']
parties = ['GERB','DPS1','DPS2','PP-DB','V','BSP','ITN','Velichie','Other']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['GERB'] != d[i]['Velichie']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
    
D = pd.concat(d.values(), ignore_index=True)
D[parties] = D[parties].astype(float)

split_date = '11 September 2024'
split_date=dateparser.parse(split_date)

fix_date = '23 September 2024'
fix_date=dateparser.parse(fix_date)

c={}
c[0]=D[(pd.to_datetime(D["Date"]) > split_date)]
c[0].rename(columns={"DPS1": "APS"}, inplace=True)
c[0].rename(columns={"DPS2": "DPS–NN"}, inplace=True)
c[0].loc[len(c[0].index)-1,['Date']] = fix_date

c[1]=D[(pd.to_datetime(D["Date"]) < split_date)]
c[1].rename(columns={"DPS1": "DPS"}, inplace=True)
c[1]=c[1].drop(["DPS2"], axis=1)

C = pd.concat(c.values(), ignore_index=True)

C.to_csv('Bulgaria/poll.csv', index=False)
