import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/44th_Quebec_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['Date','DROP','CAQ','QS','PQ','PLQ','PCQ']
parties = ['DROP','CAQ','QS','PQ','PLQ','PCQ']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-5])
  d[i]=d[i].drop(["Polling organisation","Source","Other","Sample size","Lead"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(['DROP'], axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['CAQ'] != d[i]['PCQ']]
  
headers = ['Date','CAQ','QS','PQ','PLQ','PCQ']
parties = ['CAQ','QS','PQ','PLQ','PCQ']

D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = [x.replace('–',str(np.nan)) for x in D[z]]
  D[z] = [x.replace('—',str(np.nan)) for x in D[z]]
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
  
D.to_csv('Canada/Provincial/Quebec/poll.csv', index=False)
