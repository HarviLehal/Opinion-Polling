import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Dutch_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

data=pd.DataFrame(df[0])
data=data.drop(["Polling firm", "Sample size", "Others", "Lead"], axis=1)

headers = ['Date','VVD','D66','PVV','CDA','SP','PvdA','GL','FvD','PvdD','CU','Volt','JA21','SGP','DENK','50+','BBB','BIJ1','BVNL']
parties = ['VVD','D66','PVV','CDA','SP','PvdA','GL','FvD','PvdD','CU','Volt','JA21','SGP','DENK','50+','BBB','BIJ1','BVNL']
data.columns = headers

data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data = data[data['VVD'] != data['BIJ1']]

print(data)

data.to_csv('Dutch/poll.csv', index=False)


data2=pd.DataFrame(df[0])
data2=data2.drop(["Polling firm", "Sample size", "Others", "Lead"], axis=1)

headers = ['Date','VVD','D66','PVV','CDA','SP','PvdA','GL','FvD','PvdD','CU','Volt','JA21','SGP','DENK','50+','BBB','BIJ1','BVNL']
parties = ['VVD','D66','PVV','CDA','SP','PvdA','GL','FvD','PvdD','CU','Volt','JA21','SGP','DENK','50+','BBB','BIJ1','BVNL']
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
    data2[z] = [x.replace('–','') for x in data2[z].astype(str)]
Fusie=['PvdA','GL']
data2[Fusie] = data2[Fusie].astype(float)
data2['PvdA-GL'] = data2[Fusie].sum(axis=1)
data2 = data2.drop(Fusie, axis=1)

data2 = data2[['Date','VVD','D66','PVV','PvdA-GL','CDA','SP','FvD','PvdD','CU','Volt','JA21','SGP','DENK','50+','BBB','BIJ1','BVNL']]

data2.to_csv('Dutch/poll2.csv', index=False)


