import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Australian_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers=['Date', 'Brand', 'mode', 'Sample', 'Labor','Coalition',  'Green', 'ONP', 'IND', 'Other', 'UND', 'Labor2', 'Coalition2']
parties = ['Labor', 'Coalition', 'Green', 'ONP', 'IND', 'Other', 'Labor2', 'Coalition2']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(["Brand", "Sample", "UND", "mode"], axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Labor'] != d[i]['Other']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
  d[i] = d[i].dropna(subset=['Date'])

D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
oth = ['Other','IND']
D['Other'] = D[oth].sum(axis=1)
D = D.drop('IND',axis=1)
  
PP = ['Labor2', 'Coalition2']
E = D.drop(PP, axis=1)
E.to_csv('Australia/Federal/poll.csv', index=False)


parties2 = ['Coalition', 'Labor', 'Green', 'ONP', 'Other']
D = D.drop(parties2, axis=1)
headers = ['Date', 'Labor', 'Coalition']
D.columns = headers
parties=['Labor', 'Coalition']
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)*100
D = D.drop(["total"], axis=1)
D.to_csv('Australia/Federal/poll2.csv', index=False)
