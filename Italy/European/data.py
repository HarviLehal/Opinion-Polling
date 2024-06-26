import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024_European_Parliament_election_in_Italy"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )



headers = ['Date','Lega','PD','M5S','FI','FdI','SVP','+E','IV','3','AVS','5','6','7','8']
parties = ['Lega','PD','M5S','FI','FdI','SVP','+E','IV','AVS']
drop = ['3','5','6','7','8']
e = {}
for i in range(1):
  e[i]=pd.DataFrame(df[-2])
  e[i]=e[i].drop(["Polling firm"], axis=1)
  e[i].columns = headers
  e[i]=e[i].drop(drop, axis=1)
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date2'] = [x for x in e[i]['Date2'].astype(str)]
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  e[i] = e[i][e[i]['PD'] != e[i]['SVP']]
  for z in parties: # replace any non-numeric values with NaN
    e[i][z] = [p.sub('', x) for x in e[i][z].astype(str)]
    e[i][z] = pd.to_numeric(e[i][z], errors='coerce')

e[0]['SUE']=np.where(e[0]['+E']==e[0]['IV'],e[0]['+E'],e[0]['+E']+e[0]['IV'])
threeway = ['+E','IV']
e[0] = e[0].drop(threeway, axis=1)
E = pd.concat(e.values(), ignore_index=True)

parties = ['Lega','PD','M5S','FI','FdI','SVP','AVS', 'SUE']


new_row = pd.DataFrame({'Date':'09 June 2024','Lega':8,'PD':22,'M5S':8,'FI':7,'FdI':24,'SVP':1,'AVS':6,'SUE':0}, index=[0])
E = pd.concat([new_row,E]).reset_index(drop=True)
E.Date=E.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
E['Other']=76-E[parties].sum(axis=1)

E=E[E['Other']>-1]

E.to_csv('Italy/European/poll.csv', index=False)



headers = ['Date','6','7','Lega','PD','M5S','FI','1','FdI','AVS','PTD','+E','IV','A','2','3','Libertà','4','5']
parties = ['Lega','PD','M5S','FI','FdI','AVS','PTD','+E','IV','A','Libertà']
drop = ['1','2','3','4','5','6','7']

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-3])
  d[i].columns = headers
  d[i]=d[i].drop(drop, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['AVS'] != d[i]['PD']]
  for z in parties: # replace any non-numeric values with NaN
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
split_date = '26 Mar 2024'

split_date=dateparser.parse(split_date)

c={}
c[0]=d[0][(pd.to_datetime(d[0]["Date"]) > split_date)]
c[1]=d[0][(pd.to_datetime(d[0]["Date"]) < split_date)]

c[0]['SUE']=np.where(c[0]['+E']==c[0]['IV'],c[0]['+E'],c[0]['+E']+c[0]['IV'])
threeway = ['+E','IV']
c[0] = c[0].drop(threeway, axis=1)

C = pd.concat(c.values(), ignore_index=True)

new_row = pd.DataFrame({'Date':'09 June 2024','Lega':8.7,'PD':25.8,'M5S':9.6,'FI':8.6,'FdI':28.5,'AVS':6.9,'PTD':2.3,'A':3.2,'Libertà':1.1,'SUE':3.5}, index=[0])
C = pd.concat([new_row,C]).reset_index(drop=True)
C.Date=C.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


C.to_csv('Italy/European/poll2.csv', index=False)
