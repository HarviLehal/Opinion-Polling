import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2028_South_Korean_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
p = re.compile(r'\[[a-z]+\]')
df=pd.read_html(str(tables))

headers = ['Date','DPK','PPP','RKP','NRP','PP','NFP','BIP','SDP','Other']
parties = ['DPK','PPP','RKP','NRP','PP','NFP','BIP','SDP','Other']
d = {}

for i in range(2):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(['Polling firm','Sample size','Margin of error','Und./ no ans.','Lead'], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x +str(2025-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['DPK'] != d[i]['PP']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = d[i][z].astype('float').astype(str)

D = pd.concat(d.values(), ignore_index=True)

D.to_csv('Korea/poll.csv', index=False)
