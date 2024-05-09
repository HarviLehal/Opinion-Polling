import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Japanese_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','Ishiba','Koizumi','Kono','Takaichi','Suga','Kamikawa','Kishida','Noda','Motegi','Other','Undecided']
parties = ['Ishiba','Koizumi','Kono','Takaichi','Suga','Kamikawa','Kishida','Noda','Motegi','Other','Undecided']
d = {}

for i in range(3):
  d[i]=pd.DataFrame(df[-5])
  d[i]=d[i].drop(["Sample size","Polling firm"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Kishida'] != d[i]['Undecided']]
  # d[i] = d[i][d[i]['Approve'] == d[i]['Undecided']]
  for z in parties:
    d[i][z] = d[i][z].astype('string')
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
  for z in parties:
    d[i][z] = d[i][z].astype('float')



D = pd.concat(d.values(), ignore_index=True)


D.to_csv('Japan/leadership/poll.csv', index=False)
