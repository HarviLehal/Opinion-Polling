import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_German_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))


headers = ['1','Date','2','Scholz','Merz','Neither']
parties = ['Scholz','Merz','Neither']
drops = ['1','2']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[29])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])




D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = pd.to_numeric(D[z], errors='coerce')
  
D.to_csv('German/Kanzler/poll.csv', index=False)
  

D['total']=D[parties].sum(axis=1)
D['decided']=D['total']-D['Neither']

print(D)
parties = ['Scholz','Merz']
D[parties] = D[parties].div(D['decided'], axis=0)*100

D = D.drop(["decided","total","Neither"], axis=1)

D.to_csv('German/Kanzler/poll2.csv', index=False)
