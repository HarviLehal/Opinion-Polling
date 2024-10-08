import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Nationwide_opinion_polling_for_the_2020_United_States_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','Trump', 'Biden',  '1','2','3','4','5']
parties = ['Trump', 'Biden']
drop =['1','2','3','4','5']
d = {}
for i in range(4):
  # i=j+1
  d[i]=pd.DataFrame(df[i+2])
  d[i]=d[i].drop(["Poll source","Sample size[b]","Margin of error","Lead"], axis=1)
  if i == 3:
    headers = ['Date','Trump', 'Biden',  '1','2','3','4']
    drop =['1','2','3','4']
  else:
    pass
  d[i].columns = headers
  d[i]=d[i].drop(drop, axis=1)
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[0]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i]['Date2'] = [x.split(',')[0] if len(x.split(',')) > 1 else x for x in d[i]['Date2'].astype(str)]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+' '+ str(2020) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
  
headers = ['Date','Trump', 'Biden',  '1','2']
parties = ['Trump', 'Biden']
drop =['1','2']
for j in range(1):
  i=j+4
  d[i]=pd.DataFrame(df[i+2])
  d[i]=d[i].drop(["Poll source","Sample size[b]","Margin of error","Lead"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drop, axis=1)
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D = pd.concat(d.values(), ignore_index=True)

for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
  
new_row = pd.DataFrame({'Date': '03 November 2020', 'Biden':51.31 , 'Trump':46.85}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D = D.dropna(subset=['Date'])


D.to_csv('US/old/poll.csv', index=False)


D['total']=D[parties].sum(axis=1)

D['decided']=D['total']

parties = ['Biden', 'Trump']
D[parties] = D[parties].div(D['decided'], axis=0)*100

D = D.drop(["decided","total"], axis=1)

D.to_csv('US/old/poll2.csv', index=False)
