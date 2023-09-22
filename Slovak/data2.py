import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2023_Slovak_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['drop1','Date','drop2','OĽaNO','ZĽ','Smer','SR','ĽSNS','PS','SASKA','KDH','drop4','MKP/Alliance','drop6','drop7','drop8','SPOLU/Dem','SNS','drop9','Hlas','Rep','drop10']
parties = ['OĽaNO','ZĽ','Smer','SR','ĽSNS','PS','SASKA','KDH','MKP/Alliance','SPOLU/Dem','SNS','Hlas','Rep']
drops = ['drop1','drop2','drop4','drop6','drop7','drop8','drop9','drop10']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Smer'] != d[i]['KDH']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split('%').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]

d[0]['OĽaNO-ZĽ']=np.where(d[0]['ZĽ']==d[0]['OĽaNO'], d[0]['ZĽ'], np.NaN)
d[0]['OĽaNO']=np.where(d[0]['OĽaNO']==d[0]['OĽaNO-ZĽ'], np.NaN, d[0]['OĽaNO'])
d[0]['ZĽ']=np.where(d[0]['ZĽ']==d[0]['OĽaNO-ZĽ'], np.NaN, d[0]['ZĽ'])

headers = ['drop1','Date','drop2','OĽaNO','Smer','SR','ĽSNS','PS','SPOLU/Dem','SASKA','ZĽ','KDH','drop3','MKP/Alliance','drop5','drop6','SNS','drop7','Hlas','Rep','drop8']
parties = ['OĽaNO','Smer','SR','ĽSNS','PS','SPOLU/Dem','SASKA','ZĽ','KDH','MKP/Alliance','SNS','Hlas','Rep']
drops = ['drop1','drop2','drop3','drop5','drop6','drop7','drop8']

for j in range(1):
  i = j+1
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Smer'] != d[i]['KDH']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split('%').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]

headers = ['drop1','Date','drop2','OĽaNO','Smer','SR','ĽSNS','PS','SPOLU/Dem','SASKA','ZĽ','KDH','drop3','MKP/Alliance','drop5','drop6','SNS','drop7','Hlas','Rep','drop8']
parties = ['OĽaNO','Smer','SR','ĽSNS','PS','SPOLU/Dem','SASKA','ZĽ','KDH','MKP/Alliance','SNS','Hlas','Rep']
drops = ['drop1','drop2','drop3','drop5','drop6','drop7','drop8']

for j in range(1):
  i = j+2
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Smer'] != d[i]['KDH']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split('%').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]



d[2]['SPOLU/Dem']=np.where(d[2]['SPOLU/Dem']==d[2]['PS'], np.NaN, d[2]['SPOLU/Dem'])


D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[-1,-2,-3,-4]],inplace=True)

D[parties] = D[parties].astype(float)
D = D[['Date','OĽaNO-ZĽ','OĽaNO','ZĽ','Smer','SR','ĽSNS','PS','SPOLU/Dem','SASKA','KDH','SNS','Hlas','Rep','MKP/Alliance']]

  

D.to_csv('Slovak/poll2.csv', index=False)
