import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Italian_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))


headers = ['Date','FdI','PD','M5S','Lega','FI','SUE','A','AVS','PTD','DSP','Libertà']
parties = ['FdI','PD','M5S','Lega','FI','SUE','A','AVS','PTD','DSP','Libertà']
e = {}
for i in range(1):
  e[i]=pd.DataFrame(df[i+1])
  e[i]=e[i].drop(["Polling firm","Sample size","Others","Lead","AP"], axis=1)
  e[i].columns = headers
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date2'] = [x+ str(2024-i) for x in e[i]['Date2'].astype(str)]
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  e[i] = e[i][e[i]['FdI'] != e[i]['AVS']]
  for z in parties: # replace any non-numeric values with NaN
    e[i][z] = pd.to_numeric(e[i][z], errors='coerce')

headers = ['Date','FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','Italexit','PTD','DSP','NM']
d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i+2])
  if i==0:
    d[i]=d[i].drop(["Polling firm","Sample size","Others","Lead"], axis=1)
  else:
      d[i]=d[i].drop(["Polling firm","Sample size","Others","Lead"], axis=1)
  d[i].columns = headers
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['FdI'] != d[i]['+E']]

split_date = '15 Apr 2023'

split_date=dateparser.parse(split_date)

c={}
c[0]=e[0]
c[1]=d[0]
c[2]=d[1][(pd.to_datetime(d[1]["Date"]) > split_date)]
c[3]=d[1][(pd.to_datetime(d[1]["Date"]) < split_date)]

c[3]['A-IV']=np.where(c[3]['A']==c[3]['IV'],c[3]['A'],c[3]['A']+c[3]['IV'])
threeway = ['A','IV']
c[3] = c[3].drop(threeway, axis=1)

headers = ['Date','FdI','PD','M5S','Lega','FI','A-IV','AVS','+E','Italexit','PTD','DSP','NM']
for j in range(1):
  i = j+3
  c[i+2]=pd.DataFrame(df[i+1])
  c[i+2]=c[i+2].drop(["Polling firm","Sample size","Others","Lead"], axis=1)
  c[i+2].columns = headers
  c[i+2]['Date2'] = c[i+2]['Date'].str.split('–').str[1]
  c[i+2].Date2.fillna(c[i+2].Date, inplace=True)
  c[i+2]['Date2'] = [x+ str(2022) for x in c[i+2]['Date2'].astype(str)]
  c[i+2]['Date'] = c[i+2]['Date2']
  c[i+2] = c[i+2].drop(['Date2'], axis=1)
  c[i+2].Date=c[i+2].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  c[i+2] = c[i+2][c[i+2]['FdI'] != c[i+2]['+E']]
  

C = pd.concat(c.values(), ignore_index=True)
C.to_csv('Italy/poll.csv', index=False)
