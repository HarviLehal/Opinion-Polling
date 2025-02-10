import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/2025_Kosovan_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))


headers = ['1','Date','LVV1','LVV2','LVV3','PDK','LDK','AAK1','AAK2','AAK3','2','3','SL','Others','4','5']
parties = ['LVV1','LVV2','LVV3','PDK','LDK','AAK1','AAK2','AAK3','SL','Others']
drops = ['1','2','3','4','5']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-6])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[0].loc[18,['Date']] = '14 February	2021'
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['LVV1'] != d[i]['SL']]
  d[i] = d[i].dropna(subset=['Date'])

# d[0]['Date'].replace({pd.NaT: "0 days"}, inplace=True)



D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = pd.to_numeric(D[z], errors='coerce')

AAK = ['AAK1','AAK2','AAK3']
LVV = ['LVV1','LVV2','LVV3']
D['AAK']=np.where((D['AAK1']==D['AAK2']) & (D['AAK1']==D['AAK3']),D['AAK1'], np.where(D['AAK1']==D['AAK2'],D['AAK1']+D['AAK3'],D[AAK].sum(axis=1)))
D['LVV']=D[LVV].sum(axis=1)
D = D.drop(AAK, axis=1)
D = D.drop(LVV, axis=1)

D=D[['Date','LVV','PDK','LDK','AAK','SL','Others']]


D.to_csv('Kosovo/poll.csv', index=False)
