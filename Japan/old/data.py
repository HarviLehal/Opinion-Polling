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

headers = ['Date','LDP','CDP','NIK','KMT','JCP','DPP','REI','DIY','SDP','NHK','None']
parties = ['LDP','CDP','NIK','KMT','JCP','DPP','REI','DIY','SDP','NHK','None']
d = {}

for i in range(4):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Sample size","Polling firm","Others","Und./ no ans.", "Lead"], axis=1)
  # if i < 2:
  #   d[i]=d[i].drop(["Sample size","Polling firm","FEFA","Others","Und./ no ans.", "Lead"], axis=1)
  # else:
  #   d[i]=d[i].drop(["Sample size","Polling firm","Others","Und./ no ans.", "Lead"], axis=1)
  if i==3:
    headers.remove('DIY')
    parties.remove('DIY')
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].loc[len(d[i].index)-1,['Date']] = '31 October 2021'
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['LDP'] != d[i]['KMT']]
  for z in parties:
    d[i][z] = d[i][z].astype('string')
  for z in parties:
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')

for i in range(3):
  d[i].drop(d[i].index[[-1]],inplace=True)


D = pd.concat(d.values(), ignore_index=True)
D.to_csv('Japan/poll.csv', index=False)

headers = ['Date','LDP','CDP','NIK','KMT','JCP','DPP','REI','DIY','SDP','NHK','None']
parties = ['LDP','CDP','NIK','KMT','JCP','DPP','REI','DIY','SDP','NHK','None']

D['None'].fillna(0, inplace=True)
D['total']=D[parties].sum(axis=1)

D['decided']=D['total']-D['None']

print(D)
parties = ['LDP','CDP','NIK','KMT','JCP','DPP','REI','DIY','SDP','NHK']
D[parties] = D[parties].div(D['decided'], axis=0)*100

D = D.drop(["decided","total","None"], axis=1)

D.to_csv('Japan/poll2.csv', index=False)
