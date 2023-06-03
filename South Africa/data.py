import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024_South_African_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date', 'ANC', 'DA', 'EFF', 'IFP', 'VF Plus', 'ACDP', 'Action SA']
parties = ['ANC', 'DA', 'EFF', 'IFP', 'VF Plus', 'ACDP', 'Action SA']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Polling Organisation", "Don't Know[a]","Others", "Lead", "Sample Size"], axis=1)
  d[i].columns = headers
  for z in headers:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['ANC'] != d[i]['VF Plus']]
  
D = pd.concat(d.values(), ignore_index=True)

D.to_csv('South Africa/poll.csv', index=False)
