import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Spanish_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','drop3','PSOE','PP','SMR','VOX','ERC','JxCat','PNV','EHB','drop4','drop5','drop6','drop7','drop8','drop9']
parties = ['PSOE','PP','SMR','VOX','ERC','JxCat','PNV','EHB']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7','drop8','drop9']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['PSOE'] != d[i]['EHB']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
    
headers = ['drop1','Date','drop2','drop3','PSOE','PP','VOX','UP','SMR','Cs','ERC','JxCat','PNV','EHB','drop4','drop5','drop6','drop7','drop8','drop9','drop10']
parties = ['PSOE','PP','VOX','UP','SMR','Cs','ERC','JxCat','PNV','EHB']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7','drop8','drop9','drop10']
for i in range(1):
  d[i+1]=pd.DataFrame(df[i+1])
  d[i+1].columns = headers
  d[i+1]=d[i+1].drop(drops, axis=1)
  d[i+1]['Date2'] = d[i+1]['Date'].str.split('–').str[1]
  d[i+1].Date2.fillna(d[i+1].Date, inplace=True)
  d[i+1]['Date'] = d[i+1]['Date2']
  d[i+1] = d[i+1].drop(['Date2'], axis=1)
  d[i+1].Date=d[i+1].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i+1] = d[i+1][d[i+1]['PSOE'] != d[i+1]['EHB']]
  for z in parties:
    d[i+1][z] = [p.sub('', x) for x in d[i+1][z].astype(str)]
    d[i+1][z] = d[i+1][z].str.split(' ').str[0]
    d[i+1][z] = [x.replace('–',str(np.NaN)) for x in d[i+1][z].astype(str)]
    d[i+1][z] = [x.replace('?',str(np.NaN)) for x in d[i+1][z].astype(str)]

headers = ['drop1','Date','drop2','drop3','PSOE','PP','VOX','UP','Cs','ERC','MP','JxCat','PNV','EHB','drop4','drop5','drop6','drop7','drop8','drop9','drop10']
parties = ['PSOE','PP','VOX','UP','Cs','ERC','MP','JxCat','PNV','EHB']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7','drop8','drop9','drop10']
for i in range(2):
  d[i+2]=pd.DataFrame(df[i+2])
  d[i+2].columns = headers
  d[i+2]=d[i+2].drop(drops, axis=1)
  d[i+2]['Date2'] = d[i+2]['Date'].str.split('–').str[1]
  d[i+2].Date2.fillna(d[i+2].Date, inplace=True)
  d[i+2]['Date2'] = [x+ str(2023-i) for x in d[i+2]['Date2'].astype(str)]
  d[i+2]['Date'] = d[i+2]['Date2']
  d[i+2] = d[i+2].drop(['Date2'], axis=1)
  d[i+2].Date=d[i+2].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i+2] = d[i+2][d[i+2]['PSOE'] != d[i+2]['EHB']]
  for z in parties:
    d[i+2][z] = [p.sub('', x) for x in d[i+2][z].astype(str)]
    d[i+2][z] = d[i+2][z].str.split(' ').str[0]
    d[i+2][z] = [x.replace('–',str(np.NaN)) for x in d[i+2][z].astype(str)]
    d[i+2][z] = [x.replace('?',str(np.NaN)) for x in d[i+2][z].astype(str)]

d[3].drop(d[3].index[[-1,-2,-3]],inplace=True)

wikiurl="https://en.wikipedia.org/wiki/Nationwide_opinion_polling_for_the_2023_Spanish_general_election_(2019–2021)"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
headers = ['drop1','Date','drop2','drop3','PSOE','PP','VOX','UP','Cs','ERC','MP','JxCat','PNV','EHB','drop4','drop5','drop6','drop7','drop8','drop9','drop10']
parties = ['PSOE','PP','VOX','UP','Cs','ERC','MP','JxCat','PNV','EHB']
drops = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7','drop8','drop9','drop10']
for i in range(3):
  d[i+4]=pd.DataFrame(df[i])
  d[i+4].columns = headers
  d[i+4]=d[i+4].drop(drops, axis=1)
  d[i+4]['Date2'] = d[i+4]['Date'].str.split('–').str[1]
  d[i+4].Date2.fillna(d[i+4].Date, inplace=True)
  d[i+4]['Date2'] = [x+ str(2021-i) for x in d[i+4]['Date2'].astype(str)]
  d[i+4]['Date'] = d[i+4]['Date2']
  d[i+4] = d[i+4].drop(['Date2'], axis=1)
  d[i+4].Date=d[i+4].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i+4] = d[i+4][d[i+4]['PSOE'] != d[i+4]['EHB']]
  for z in parties:
    d[i+4][z] = [p.sub('', x) for x in d[i+4][z].astype(str)]
    d[i+4][z] = d[i+4][z].str.split(' ').str[0]
    d[i+4][z] = [x.replace('–',str(np.NaN)) for x in d[i+4][z].astype(str)]
    d[i+4][z] = [x.replace('?',str(np.NaN)) for x in d[i+4][z].astype(str)]


D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[-1,-3]],inplace=True)

Sumar = ['SMR', 'UP', 'MP']
parties = ['PSOE','PP','VOX','SMR','ERC','JxCat','PNV','EHB','MP','UP','Cs']
D[parties] = D[parties].apply(lambda x: x.str.strip()).replace('', np.nan)
D = D.drop(D[D["PSOE"]=='29.0nan'].index)
D[parties] = D[parties].astype(float)
D['Sumar'] = D[Sumar].sum(axis=1)
D = D.drop(Sumar, axis=1)
D = D.drop(D[D["Sumar"]==38.4].index)
D = D.drop(D[D["Date"]==dateparser.parse('2022-12-22')].index)

new_row = pd.DataFrame({'Date':'24 July 2023','PSOE':31.71,'PP':33.01,'VOX':12.39,'ERC':1.89,'JxCat':1.6,'PNV':1.13,'EHB':1.36,'Cs':np.nan,'Sumar':12.31}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.drop(D.index[[1,2,3]],inplace=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D = D[['Date','PSOE','PP','Sumar','VOX','ERC','JxCat','PNV','EHB', 'Cs']]


D.to_csv('Spain/poll.csv', index=False)

Left = ['Sumar','PSOE','PNV','EHB','ERC']
Right = ['PP','VOX']
D['Govt (PSOE + Sumar + EHB + ERC + PNV)'] = D[Left].sum(axis=1)
D['Right (PP + VOX)'] = D[Right].sum(axis=1)
D = D.drop(Left + Right, axis=1)
D = D.drop(D[D['Govt (PSOE + Sumar + EHB + ERC + PNV)'] < 34].index)
D.to_csv('Spain/poll2.csv', index=False)
