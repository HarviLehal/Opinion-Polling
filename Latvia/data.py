import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Next_Latvian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
headers = ['1','Date','2','JV','ZZS','AS','NA','ST!','LPV','PRO','KP','LA','S','P21','LKS','SV','JKP','3','4']
parties = ['JV','ZZS','AS','NA','ST!','LPV','PRO','KP','LA','S','P21','LKS','SV','JKP']
drops = ['1','2','3','4']
d = {}
for i in range(4):
  d[i]=pd.DataFrame(df[i+1])
  if i==3:
    d[i]=d[i].drop(['R'], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'last'}))
  d[i] = d[i][d[i]['JV'] != d[i]['JKP']]
  d[i] = d[i].dropna(subset=['Date'])

d[3]=d[3].drop(['LA'],axis=1)
d[3].rename(columns={'KP':'AP!'},inplace=True)


D = pd.concat(d.values(), ignore_index=True)
parties = ['JV','ZZS','AS','NA','ST!','LPV','PRO','KP','LA','S','P21','LKS','SV','JKP','AP!']
for z in parties:
  D[z] = pd.to_numeric(D[z], errors='coerce')

  

D.to_csv('Latvia/poll.csv', index=False)
