import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Next_Croatian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers=['Date','1','2','HDZ', 'SDP', 'DP','DOMiNO', 'PiP', 'Možemo', 'Most', 'HS', 'Fokus', 'IDS','NPS','RF','Centar','HSS','HSU','HNS','Other','UND','3']
parties = ['HDZ', 'SDP', 'DP','DOMiNO', 'PiP', 'Možemo', 'Most', 'HS', 'Fokus', 'IDS','NPS','RF','Centar','HSS','HSU','HNS','Other','UND']
drops = ['1','2','3']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  # d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  # d[i]['Date'] = d[i]['Date2']
  # d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['HDZ'])

D = pd.concat(d.values(), ignore_index=True)

D['DOMiNO']=np.where(D['DOMiNO']>4.5,np.nan,D['DOMiNO'])
D['PiP']=np.where(D['PiP']>9.5,np.nan,D['PiP'])
D['HS']=np.where(D['HS']>7.9,np.nan,D['HS'])
D['Other']=np.where(np.isnan(D['Other'])==True,0,D['Other'])

parties = ['HDZ', 'SDP', 'DP','DOMiNO', 'PiP', 'Možemo', 'Most', 'HS', 'Fokus', 'IDS','NPS','RF','Centar','HSS','HSU','HNS','UND']
D['total']=D[parties].sum(axis=1)
D['Others']=100-D['total']
parties = ['HDZ', 'SDP', 'DP','DOMiNO', 'PiP', 'Možemo', 'Most', 'HS', 'Fokus', 'IDS','NPS','RF','Centar','HSS','HSU','HNS','Other','UND','Others']
for z in parties:
  D[z] = pd.to_numeric(D[z], errors='coerce')

# D[parties]=D[parties].div(D['total'], axis=0)
D = D.drop(['total','UND','Other'], axis=1)



D.to_csv('Croatia/poll2.csv', index=False)
