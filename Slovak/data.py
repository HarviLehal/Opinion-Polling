import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Slovak_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','Smer','PS','Hlas','OLaNOap1','OLaNOap2','OLaNOap3','KDH','SASKA','SNS','Republika','Aliancia','Demokrati','SR','ĽSNS','drop3','drop4']
parties = ['Smer','PS','Hlas','OLaNOap1','OLaNOap2','OLaNOap3','KDH','SASKA','SNS','Republika','Aliancia','Demokrati','SR','ĽSNS']
drops = ['drop1','drop2','drop3','drop4']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i][d[i]['Date'] != '8 Jun 2024']
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Smer'] != d[i]['SR']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split('%').str[0]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z].astype(str)]
# d[0].drop(d[0].index[[-1]],inplace=True)


D = pd.concat(d.values(), ignore_index=True)

D[parties] = D[parties].astype(float)

Slovensko=['OLaNOap1','OLaNOap2','OLaNOap3']

D['OĽaNOap']=np.where((D['OLaNOap1']==D['OLaNOap2']) & (D['OLaNOap1']==D['OLaNOap3']),D['OLaNOap1'], np.where(D['OLaNOap1']==D['OLaNOap2'],D['OLaNOap1']+D['OLaNOap3'],D[Slovensko].sum(axis=1)))

D= D[['Date','Smer','PS','Hlas','OĽaNOap','KDH','SASKA','SNS','Republika','Aliancia','Demokrati','SR','ĽSNS']]

D.to_csv('Slovak/poll.csv', index=False)
