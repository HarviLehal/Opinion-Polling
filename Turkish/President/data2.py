import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://tr.wikipedia.org/wiki/Bir_sonraki_T%C3%BCrkiye_cumhurba%C5%9Fkanl%C4%B1%C4%9F%C4%B1_se%C3%A7imi_i%C3%A7in_yap%C4%B1lan_anketler"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')
p = re.compile(r'\[[a-z 0-9]+\]'  )

d = {}
for i in range(1):
  print(i)
  heads = []
  for j in range(len(df[i+3].columns)):
    heads.append(df[i+3].columns[j][0])
  heads = [p.sub('', x) for x in heads]
  d[i]=pd.DataFrame(df[i+3])
  d[i].columns = heads
  parties = heads[3:-1]
  d[i] = d[i].drop(d[i].columns[[1, 2,-1]],axis = 1)
  d[i].rename(columns={d[i].columns[0]: 'Date'}, inplace=True)
  d[i]['Date2'] = d[i]['Date'].str.split('-').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+' '+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  for z in parties:
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
    # d[i][z] = np.where(d[i][z]>100)
  d[i] = d[i].dropna(subset=[d[i].columns[1]])
# d[2] = d[2].drop(['MP'], axis=1)
for i in range(1):
  d[i]=d[i].reset_index(drop=True)

D = pd.concat(d.values(), ignore_index=True)

# Split the DataFrame after each year row
split_points = D[D['Date'].isin(['2025', '2024'])].index
parts = []
prev_idx = 0

for idx in split_points:
    part = D.iloc[prev_idx:idx]
    year = D.at[idx, 'Date']
    part['Date'] = part['Date'] + ' ' + year
    parts.append(part)
    prev_idx = idx + 1

# Add the remaining part after the last year row
parts.append(D.iloc[prev_idx:])

# Concatenate the parts and reset the index
D = pd.concat(parts).reset_index(drop=True)




D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, languages=['tr'], settings={'PREFER_DAY_OF_MONTH': 'first'}))
# D['Date'] = D['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
D['Date'] = D['Date'].apply(lambda x: x.date())
# D['Date'] = D['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

D.to_csv('Turkish/President/poll2.csv', index=False)



d = {}
for i in range(1):
  print(i)
  heads = []
  for j in range(len(df[i+6].columns)):
    heads.append(df[i+6].columns[j][0])
  heads = [p.sub('', x) for x in heads]
  d[i]=pd.DataFrame(df[i+6])
  d[i].columns = heads
  parties = heads[3:-1]
  d[i] = d[i].drop(d[i].columns[[1, 2,-1]],axis = 1)
  d[i].rename(columns={d[i].columns[0]: 'Date'}, inplace=True)
  d[i]['Date2'] = d[i]['Date'].str.split('-').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+' '+ str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  for z in parties:
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
    # d[i][z] = np.where(d[i][z]>100)
  d[i] = d[i].dropna(subset=[d[i].columns[1]])
# d[2] = d[2].drop(['MP'], axis=1)
for i in range(1):
  d[i]=d[i].reset_index(drop=True)

D = pd.concat(d.values(), ignore_index=True)

# Split the DataFrame after each year row
split_points = D[D['Date'].isin(['2025', '2024'])].index
parts = []
prev_idx = 0

for idx in split_points:
    part = D.iloc[prev_idx:idx]
    year = D.at[idx, 'Date']
    part['Date'] = part['Date'] + ' ' + year
    parts.append(part)
    prev_idx = idx + 1

# Add the remaining part after the last year row
parts.append(D.iloc[prev_idx:])

# Concatenate the parts and reset the index
D = pd.concat(parts).reset_index(drop=True)




D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, languages=['tr'], settings={'PREFER_DAY_OF_MONTH': 'first'}))
# D['Date'] = D['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
D['Date'] = D['Date'].apply(lambda x: x.date())
# D['Date'] = D['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

D.to_csv('Turkish/President/poll3.csv', index=False)
