import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2028_Lithuanian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['1','Date','2','LSDP','TS-LKD','PPNA','DSVL','LS','LVŽS','LP','LLRA−KŠS','NS','DP','LRP','LŽP','TTS','PLT','3']
parties = ['LSDP','TS-LKD','PPNA','DSVL','LS','LVŽS','LP','LLRA−KŠS','NS','DP','LRP','LŽP','TTS','PLT']
drops = ['1','2','3']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i].columns = headers
  for z in headers:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])

# d[0]['Date'].replace({pd.NaT: "0 days"}, inplace=True)



D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].str.strip('%')
  D[z] = pd.to_numeric(D[z], errors='coerce')
D = D.dropna(subset=['LSDP'])

other = ['LLRA−KŠS','NS','DP','LRP','LŽP','TTS','PLT']
D['others']=D[other].sum(axis=1)
for i in other:
  D[i]=np.where(D['others']>30, np.nan, D[i])
D = D.drop(['others'], axis=1)
D.loc[1,['LP']] = np.nan


D.to_csv('Lithuanian/poll.csv', index=False)
