import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2027_South_Korean_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
p = re.compile(r'\[[a-z]+\]')
df=pd.read_html(str(tables))

headers = ['Date','Lee Jae-myung','Kim Dong-yeon','Han Dong-hoon','Oh Se-hoon','Hong Joon-pyo','1','Won Hee-ryong','Anh Cheol-soo','Cho Kuk','Lee Jun-seok','Lee Nak-yon']
parties = ['Lee Jae-myung','Kim Dong-yeon','Han Dong-hoon','Oh Se-hoon','Hong Joon-pyo','Won Hee-ryong','Anh Cheol-soo','Cho Kuk','Lee Jun-seok','Lee Nak-yon']
drops = ['1']
d = {}

for i in range(1):
  d[i]=pd.DataFrame(df[-2])
  d[i]=d[i].drop(['Polling firm','Sample size','Margin of error','Und./ no ans.','Lead','Others'], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Cho Kuk'] != d[i]['Lee Jae-myung']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = d[i][z].astype('float').astype(str)

D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[-1]],inplace=True)

D.to_csv('Korea/poll2.csv', index=False)




headers = ['Date','Lee Jae-myung','Han Dong-hoon','Others']
parties = ['Lee Jae-myung','Han Dong-hoon','Others']
drops = ['1']
d = {}

for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i]=d[i].drop(['Polling firm','Sample size','Margin of error','Und./ no ans.','Lead'], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Han Dong-hoon'] != d[i]['Others']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = d[i][z].astype('float').astype(str)

D = pd.concat(d.values(), ignore_index=True)

new_row = pd.DataFrame({'Date': '09 Mar 2022', 'Lee Jae-myung':47.83, 'Han Dong-hoon':48.56, 'Others':3.61}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].astype('float')

D['Others'].fillna(0, inplace=True)
D['total']=D[parties].sum(axis=1)


D[parties] = D[parties].div(D['total'], axis=0)*100

D = D.drop(["total"], axis=1)

D.to_csv('Korea/poll3.csv', index=False)
