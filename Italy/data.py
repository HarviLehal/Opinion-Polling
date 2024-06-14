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
for i in range(2):
  e[i]=pd.DataFrame(df[i+1])
  if i ==0:
    e[i]=e[i].drop(["Polling firm","Sample size","Others","Lead"], axis=1)
  else:
    e[i]=e[i].drop(["Polling firm","Sample size","Others","Lead","AP"], axis=1)
  e[i].columns = headers
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date2'] = [x+ str(2024) for x in e[i]['Date2'].astype(str)]
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  e[i] = e[i][e[i]['FdI'] != e[i]['AVS']]
  for z in parties: # replace any non-numeric values with NaN
    e[i][z] = pd.to_numeric(e[i][z], errors='coerce')
e[1].drop(e[1].index[[0]],inplace=True)

headers = ['Date','FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','Italexit','PTD','DSP','NM']
d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i+3])
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
c[1]=e[1]
c[2]=d[0]
c[3]=d[1][(pd.to_datetime(d[1]["Date"]) > split_date)]
c[4]=d[1][(pd.to_datetime(d[1]["Date"]) < split_date)]

c[4]['A-IV']=np.where(c[4]['A']==c[4]['IV'],c[4]['A'],c[4]['A']+c[4]['IV'])
threeway = ['A','IV']
c[4] = c[4].drop(threeway, axis=1)

headers = ['Date','FdI','PD','M5S','Lega','FI','A-IV','AVS','+E','Italexit','PTD','DSP','NM']
c[5]=pd.DataFrame(df[-1])
c[5]=c[5].drop(["Polling firm","Sample size","Others","Lead"], axis=1)
c[5].columns = headers
c[5]['Date2'] = c[5]['Date'].str.split('–').str[1]
c[5].Date2.fillna(c[5].Date, inplace=True)
c[5]['Date2'] = [x+ str(2022) for x in c[5]['Date2'].astype(str)]
c[5]['Date'] = c[5]['Date2']
c[5] = c[5].drop(['Date2'], axis=1)
c[5].Date=c[5].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
c[5] = c[5][c[5]['FdI'] != c[5]['+E']]
  

C = pd.concat(c.values(), ignore_index=True)
C.to_csv('Italy/poll.csv', index=False)
