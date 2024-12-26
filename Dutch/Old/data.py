import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Dutch_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

data2=pd.DataFrame(df[0])
data2=data2.drop(["Polling firm", "Sample size", "Lead","Ref"], axis=1)

headers = ['Date','VVD','D66','PVV','CDA','SP','PvdA','GL','FvD','PvdD','CU','Volt','JA21','SGP','DENK','50+','BBB','BIJ1','BVNL','NSC']
parties = ['VVD','D66','PVV','CDA','SP','PvdA','GL','FvD','PvdD','CU','Volt','JA21','SGP','DENK','50+','BBB','BIJ1','BVNL','NSC']
data2.columns = headers

data2['Date2'] = data2['Date'].str.split('–').str[1]
data2.Date2.fillna(data2['Date'].str.split('-').str[1], inplace=True)
data2.Date2.fillna(data2.Date, inplace=True)
data2.Date = data2.Date2
data2 = data2.drop(['Date2'],axis=1)
data2.Date = data2['Date'].astype(str)
data2.Date = data2.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data2 = data2[data2['VVD'] != data2['BIJ1']]
for z in parties:
  data2[z] = [p.sub('', x) for x in data2[z].astype(str)]
  data2[z] = [x.replace('–',str(np.nan)) for x in data2[z].astype(str)]
  data2[z] = [x.replace('–',str(np.nan)) for x in data2[z].astype(str)]
data2[parties] = data2[parties].astype(float)
data2['PvdA']=np.where(data2['PvdA']>18, 0, data2['PvdA'])
Fusie=['PvdA','GL']
data2[Fusie] = data2[Fusie].astype(float)
data2['PvdA-GL'] = data2[Fusie].sum(axis=1)
data2 = data2.drop(Fusie, axis=1)

data2 = data2[['Date','VVD','D66','PVV','PvdA-GL','CDA','SP','FvD','PvdD','CU','Volt','JA21','SGP','DENK','50+','BBB','BIJ1','BVNL','NSC']]
data2.drop(data2.index[[1,2]],inplace=True)

# new_row = pd.DataFrame({'Date': '22 Nov 2023', 'VVD':24, 'D66':9, 'PVV':37, 'PvdA-GL':25, 'CDA':5, 'SP':5, 'FvD':3, 'PvdD':3, 'CU':3, 'Volt':2, 'JA21':1, 'SGP':3, 'DENK':3, '50+':0, 'BBB':7, 'BIJ1':0, 'BVNL':0, 'NSC':20}, index=[0])
# new_row.Date=new_row.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# data2 = pd.concat([new_row,data2]).reset_index(drop=True)

data2.to_csv('Dutch/poll.csv', index=False)


