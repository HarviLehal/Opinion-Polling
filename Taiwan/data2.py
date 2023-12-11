import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024_Taiwanese_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )
q = re.compile(r'\[\d+\]')

headers = ['Date','DPP','KMT','TPP','Other']
parties = ['DPP','KMT','TPP','Other']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[7])
  d[i]=d[i].drop(["Pollster", "Sample size"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['DPP'] != d[i]['TPP']]

headers = ['Date','DPP','KMT','TPP','Ind','Other']
parties = ['DPP','KMT','TPP','Ind','Other']
d = {}
for j in range(1):
  i = j+1
  d[i]=pd.DataFrame(df[8])
  d[i]=d[i].drop(["Pollster", "Sample size"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['DPP'] != d[i]['TPP']]

  

D = pd.concat(d.values(), ignore_index=True)

for z in parties:
    D[z] = [p.sub('', x) for x in D[z].astype(str)]
    D[z] = [q.sub('', x) for x in D[z].astype(str)]
    D[z] = D[z].str.strip('%')
    D[z] = [x.replace('–',str(np.NaN)) for x in D[z].astype(str)]
    D[z] = [x.replace('—',str(np.NaN)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)
D=D.drop(D[D['Ind'] > 0].index)
D=D.drop('Ind', axis=1)
D.reset_index(drop=True)


parties = ['DPP','KMT','TPP']

D['Other'].fillna(0, inplace=True)
D['total']=D[parties].sum(axis=1)

D['decided']=D['total']-D['Other']

print(D)
D[parties] = D[parties].div(D['total'], axis=0)*100

D = D.drop(["decided","total","Other"], axis=1)
# new_row = pd.DataFrame({'Date': '11 Jan 2020', 'DPP':57.13 , 'KMT':38.61 , 'TPP':np.NaN}, index=[0])
# new_row.Date=new_row.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# D = pd.concat([new_row,D]).reset_index(drop=True)
# D.to_csv('Taiwan/poll2.csv', index=False)


D.to_csv('Taiwan/polla.csv', index=False)

new_row = pd.DataFrame({'Date': '11 Jan 2020', 'DPP':57.13 , 'KMT':38.61 , 'TPP':np.NaN}, index=[0])
new_row.Date=new_row.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D = pd.concat([new_row,D]).reset_index(drop=True)

D.to_csv('Taiwan/poll2a.csv', index=False)
