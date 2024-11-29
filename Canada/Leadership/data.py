import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_45th_Canadian_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','Trudeau','Poilievre','Singh','Blanchet','May','Bernier']
parties = ['Trudeau','Poilievre','Singh','Blanchet','May','Bernier']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-4])
  d[i]=d[i].drop(["Polling firm", "Link", "Unsure", "Margin of error[c]", "Lead"], axis=1)
  d[i].columns = headers
  # d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  # d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  # d[i]['Date'] = d[i]['Date2']
  # d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Poilievre'] != d[i]['Blanchet']]
  d[i].drop(d[i].index[[-1,-2,-4]],inplace=True)
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  
D = pd.concat(d.values(), ignore_index=True)
D = D.dropna(subset=['Singh'])
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)*100
D = D.drop(["total"], axis=1)
D.to_csv('Canada/Leadership/poll.csv', index=False)
