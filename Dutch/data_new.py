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

D=pd.DataFrame(df[1])
D=D.drop(["Polling firm", "Sample size", "Lead","Ref"], axis=1)

headers = ['Date','PVV','PvdA','GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']
parties = ['PVV','PvdA','GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']
headers = ['Date','PVV','PvdA-GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']
parties = ['PVV','PvdA-GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']
D.columns = headers

D['Date2'] = D['Date'].str.split('–').str[1]
D.Date2.fillna(D['Date'].str.split('-').str[1], inplace=True)
D.Date2.fillna(D.Date, inplace=True)
D.Date = D.Date2
D = D.drop(['Date2'],axis=1)
D.Date = D['Date'].astype(str)
D.Date = D.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D = D[D['PVV'] != D['SGP']]
for z in parties:
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
  D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)
# D['PvdA']=np.where(D['PvdA']==D['GL'], 0, D['PvdA'])
# Fusie=['PvdA','GL']
# D[Fusie] = D[Fusie].astype(float)
# D['PvdA-GL'] = D[Fusie].sum(axis=1)
# D = D.drop(Fusie, axis=1)

D = D[['Date','PVV','PvdA-GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']]

D.to_csv('Dutch/poll_new.csv', index=False)



parties= ['PVV','PvdA-GL','VVD','NSC','D66','BBB','CDA','SP','DENK','PvdD','FvD','SGP','CU','Volt','JA21']

govt = ['PVV','VVD','NSC','BBB']

D[parties] = D[parties].astype(float)
D['Government'] = D[govt].sum(axis=1)
D['Opposition'] = 150- D['Government']

D = D.drop(parties, axis=1)

D.to_csv('Dutch/poll_govt.csv', index=False)
