import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://tr.wikipedia.org/wiki/Bir_sonraki_Türkiye_genel_seçimleri_için_yapılan_anketler"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')

headers = ['Date', 'AKP', 'CHP', 'MHP', 'İYİ', 'DEM', 'YRP', 'ZP', 'TİP']
parties = ['AKP', 'CHP', 'MHP', 'İYİ', 'DEM', 'YRP', 'ZP', 'TİP']

d = {}
for i in range(2):
  if i == 1:
    headers = ['Date', 'AKP', 'CHP', 'MHP', 'İYİ', 'DEM', 'YRP', 'ZP', 'TİP', 'MP']
    parties = ['AKP', 'CHP', 'MHP', 'İYİ', 'DEM', 'YRP', 'ZP', 'TİP', 'MP']
  d[i]=pd.DataFrame(df[i])
  d[i] = d[i].drop(['Anket şirketi','Örneklem','Diğer','Fark'], axis=1)
  d[i].columns = headers
  d[i] = d[i][d[i]['AKP'] != d[i]['DEM']]
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i]['Date2'] = d[i]['Date'].str.split('-').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+' '+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  for z in parties:
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
  d[i][parties] = d[i][parties].astype(float)
d[1] = d[1].drop(['MP'], axis=1)
# d[1] = d[1].drop(['DEVA'], axis=1)
for i in range(2):
  d[i]=d[i].reset_index(drop=True)

d[0].loc[len(d[0].index)-12,['Date']] = ' 1 May 2024'
d[0].loc[len(d[0].index)-5,['Date']] = ' 1 Nis 2024'
d[0].loc[len(d[0].index)-3,['Date']] = ' 5 Mar 2024'
d[1].loc[len(d[1].index)-1,['Date']] = '14 Mayıs 2023'

d[0].drop(d[0].index[[-1]],inplace=True)
d[0] = d[0][d[0]['Date'] != '31 Mart 2024']

D = pd.concat(d.values(), ignore_index=True)

D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D['Date']= D['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
D
D.to_csv('Turkish/poll.csv', index=False)

