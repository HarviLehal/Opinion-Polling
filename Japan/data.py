import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Japanese_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','1','2','LDP','CDP','DPFP','NIK','KMT','REI','JCP','DIY','CPJ','SDP','3','None','4','5']
parties = ['LDP','CDP','DPFP','NIK','KMT','REI','JCP','DIY','CPJ','SDP','None']
drops = ['1','2','3','4','5']
d = {}
for i in range(2):
  heads = []
  for j in range(len(df[i+1].columns)):
    heads.append(df[i+1].columns[j][0])
  d[i]=pd.DataFrame(df[i+1])
  d[i].columns = heads
  # parties.remove("Others")
  # parties.replace('No Party', 'None')
  d[i].rename(columns={'No party': 'None','Fieldwork date':'Date','Ishin':'NIK','Reiwa':'REI','Komei':'KMT'}, inplace=True)
  d[i] = d[i].drop(d[i].columns[[1, 2,-1,-2,-4]],axis = 1)
  parties = d[i].columns[1:]
  # d[i]=pd.DataFrame(df[i+1])
  # d[i].columns = headers
  # d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['LDP'] != d[i]['SDP']]
  d[i] = d[i].dropna(subset=['Date'])



D = pd.concat(d.values(), ignore_index=True)
D = D[['Date','LDP','CDP','DPFP','NIK','KMT','REI','JCP','DIY','CPJ','SDP','None']]
parties=['LDP','CDP','DPFP','NIK','KMT','REI','JCP','DIY','CPJ','SDP','None']
for z in parties:
  D[z] = pd.to_numeric(D[z], errors='coerce')
D.drop(D.index[[-1]],inplace=True)

  

D.to_csv('Japan/poll.csv', index=False)
