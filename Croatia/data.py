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


headers=['Date','1','2','HDZ', 'SDP', 'DP', '3', 'Možemo', 'Most', 'O1', 'O2', 'O3','O4','O5','O6','O7','O8','O9','O10','4','5']
parties = ['HDZ', 'SDP', 'DP', 'Možemo', 'Most', 'O1', 'O2', 'O3','O4','O5','O6','O7','O8','O9','O10']
drops = ['1','2','3','4','5']
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
  d[i] = d[i][d[i]['HDZ'] != d[i]['Most']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]

D = pd.concat(d.values(), ignore_index=True)

for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
Others =['O1', 'O2', 'O3','O4','O5','O6','O7','O8','O9','O10']
D['O1']=np.where(D['O1']==D['Most'],np.nan,D['O1'])
D['Others']=D[Others].sum(axis=1)
D = D.drop(Others, axis=1)

parties = ['HDZ', 'SDP', 'DP', 'Možemo', 'Most','Others']
D['total']=D[parties].sum(axis=1)
D[parties]=D[parties].div(D['total'], axis=0)
D = D.drop(['total'], axis=1)



D.to_csv('Croatia/poll.csv', index=False)
