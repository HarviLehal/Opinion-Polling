import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Greek_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','ΝΔ','ΣΥΡΙΖΑ','ΠΑΣΟΚ - ΚΙΝΑΛ','KKE','ΕΛ','ΜέΡΑ25']
parties = ['ΝΔ','ΣΥΡΙΖΑ','ΠΑΣΟΚ - ΚΙΝΑΛ','KKE','ΕΛ','ΜέΡΑ25']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Polling firm/Commissioner","Sample size","XA","EKE","ED","Lead"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['ΝΔ'] != d[i]['KKE']]
  for z in parties:
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–','') for x in d[i][z].astype(str)]
    
d[0].drop(d[0].index[[0,2,-1,-3]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
# new_row = pd.DataFrame({'Date': '21 May 2023', 'ΝΔ':40.81 , 'ΣΥΡΙΖΑ':20.06 , 'ΠΑΣΟΚ - ΚΙΝΑΛ':11.58 , 'KKE':7.18, 'ΕΛ':4.47, 'ΜέΡΑ25':2.58}, index=[0])
# D = pd.concat([new_row,D]).reset_index(drop=True)
# D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D.to_csv('Greece/poll.csv', index=False)

Left = ['ΣΥΡΙΖΑ', 'KKE', 'ΜέΡΑ25','ΠΑΣΟΚ - ΚΙΝΑΛ']
Right = ['ΝΔ','ΕΛ']
D[parties] = D[parties].astype(float)
D['Αριστερά  (ΣΥΡΙΖΑ+ KKE+ ΜέΡΑ25+ ΠΑΣΟΚ)'] = D[Left].sum(axis=1)
D['Δεξιά     (ΝΔ+ΕΛ)'] = D[Right].sum(axis=1)
D = D.drop(Left+Right, axis=1)



D.to_csv('Greece/poll2.csv', index=False)
