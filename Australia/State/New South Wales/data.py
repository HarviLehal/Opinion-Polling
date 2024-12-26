import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2027_New_South_Wales_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers=['Date', 'Firm', 'Labor', 'LNP', 'Green', 'ONP', 'Other', 'Labor2', 'Coalition2']
parties = ['Labor', 'LNP', 'Green', 'Other', 'Labor2', 'Coalition2']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i].columns = headers
  d[i]=d[i].drop(["Firm","ONP"], axis=1)
  d[0].loc[len(d[0].index)-1,['Date']] = '25 March 2023'
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Labor'] != d[i]['Other']]
  for z in parties:
    d[i][z] = d[i][z].str.split('%').str[0]
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = d[i][z].astype('float')
    
D = pd.concat(d.values(), ignore_index=True)
PP = ['Labor2', 'Coalition2']
E = D.drop(PP, axis=1)
E.to_csv('Australia/State/New South Wales/poll.csv', index=False)


parties2 = ['Labor', 'LNP', 'Green', 'Other']
D = D.drop(parties2, axis=1)
headers = ['Date', 'Labor', 'LNP']
D.columns = headers
D.to_csv('Australia/State/New South Wales/poll2.csv', index=False)
