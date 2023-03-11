import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date', 'Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform']
parties = ['Con', 'Lab', 'Lib Dem', 'SNP', 'Green', 'Reform']
d = {}
for i in range(4):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Pollster", "Client", "Area", "Others", "Lead", "Sample size"], axis=1)
  d[i].columns = headers
  for z in headers:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–','-') for x in d[i][z]]
    d[i][z] = [x.replace('TBC','-') for x in d[i][z]]
    d[i][z] = [x.replace('?','-') for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  d[i] = d[i][d[i]['Con'] != d[i]['Reform']]
  
D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[-2]],inplace=True)
D.loc[len(D.index),['Date']] = '12 Dec 2019'

D.to_csv('UK/general_polling/poll.csv', index=False)
