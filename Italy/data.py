import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Italian_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','Italexit']
parties = ['FdI','PD','M5S','Lega','FI','A','IV','+E','Italexit']
d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i])
  if i==0:
    d[i]=d[i].drop(["Polling firm","Sample size","PTD[b]","DSP","NM","Others","Lead"], axis=1)
  else:
      d[i]=d[i].drop(["Polling firm","Sample size","UP","DSP","NM","Others","Lead"], axis=1)
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
c[0]=d[0]
c[1]=d[1][(pd.to_datetime(d[1]["Date"]) > split_date)]
c[2]=d[1][(pd.to_datetime(d[1]["Date"]) < split_date)]

c[2]['A-IV']=np.where(c[2]['A']==c[2]['IV'],c[2]['A'],c[2]['A']+c[2]['IV'])
threeway = ['A','IV']
c[2] = c[2].drop(threeway, axis=1)

headers = ['Date','FdI','PD','M5S','Lega','FI','A-IV','AVS','+E','Italexit']
parties = ['FdI','PD','M5S','Lega','FI','A-IV','+E','Italexit']
for j in range(1):
  i = j+2
  c[i+2]=pd.DataFrame(df[i])
  c[i+2]=c[i+2].drop(["Polling firm","Sample size","UP","ISP","NM","Others","Lead"], axis=1)
  c[i+2].columns = headers
  c[i+2]['Date2'] = c[i+2]['Date'].str.split('–').str[1]
  c[i+2].Date2.fillna(c[i+2].Date, inplace=True)
  c[i+2]['Date2'] = [x+ str(2024-i) for x in c[i+2]['Date2'].astype(str)]
  c[i+2]['Date'] = c[i+2]['Date2']
  c[i+2] = c[i+2].drop(['Date2'], axis=1)
  c[i+2].Date=c[i+2].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  c[i+2] = c[i+2][c[i+2]['FdI'] != c[i+2]['+E']]
  

C = pd.concat(c.values(), ignore_index=True)
C.to_csv('Italy/poll.csv', index=False)
