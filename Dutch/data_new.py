import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Next_Dutch_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

data2=pd.DataFrame(df[1])
data2=data2.drop(["Polling firm", "Sample size", "Lead","Ref"], axis=1)

headers = ['Date','PVV','PvdA','GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']
parties = ['PVV','PvdA','GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']
data2.columns = headers

data2['Date2'] = data2['Date'].str.split('–').str[1]
data2.Date2.fillna(data2['Date'].str.split('-').str[1], inplace=True)
data2.Date2.fillna(data2.Date, inplace=True)
data2.Date = data2.Date2
data2 = data2.drop(['Date2'],axis=1)
data2.Date = data2['Date'].astype(str)
data2.Date = data2.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data2 = data2[data2['PVV'] != data2['SGP']]
for z in parties:
  data2[z] = [p.sub('', x) for x in data2[z].astype(str)]
  data2[z] = [x.replace('–',str(np.NaN)) for x in data2[z].astype(str)]
  data2[z] = [x.replace('–',str(np.NaN)) for x in data2[z].astype(str)]
data2[parties] = data2[parties].astype(float)
data2['PvdA']=np.where(data2['PvdA']==data2['GL'], 0, data2['PvdA'])
Fusie=['PvdA','GL']
data2[Fusie] = data2[Fusie].astype(float)
data2['PvdA-GL'] = data2[Fusie].sum(axis=1)
data2 = data2.drop(Fusie, axis=1)

data2 = data2[['Date','PVV','PvdA-GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']]



# '''CORRECTION'''
# headers = ['Date','PVV','PvdA-GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']
# parties = ['PVV','PvdA-GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']
# data2.columns = headers
# 
# data2['Date2'] = data2['Date'].str.split('–').str[1]
# data2.Date2.fillna(data2['Date'].str.split('-').str[1], inplace=True)
# data2.Date2.fillna(data2.Date, inplace=True)
# data2.Date = data2.Date2
# data2 = data2.drop(['Date2'],axis=1)
# data2.Date = data2['Date'].astype(str)
# data2.Date = data2.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# data2 = data2[data2['PVV'] != data2['SGP']]
# for z in parties:
#   data2[z] = [p.sub('', x) for x in data2[z].astype(str)]
#   data2[z] = [x.replace('–',str(np.NaN)) for x in data2[z].astype(str)]
#   data2[z] = [x.replace('–',str(np.NaN)) for x in data2[z].astype(str)]
# data2[parties] = data2[parties].astype(float)
# 
# data2 = data2[['Date','PVV','PvdA-GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']]
# 


data2.to_csv('Dutch/poll_new.csv', index=False)


