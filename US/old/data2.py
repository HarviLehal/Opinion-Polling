import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Nationwide_opinion_polling_for_the_2016_United_States_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['1','Date','Clinton','Trump','2','3','4']
parties = ['Clinton','Trump']
drop =['1','2','3','4']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[i+1])
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
  d[i]['Date2'] = [x+' '+ str(2016) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
D = pd.concat(d.values(), ignore_index=True)

for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')

new_row = pd.DataFrame({'Date': '08 November 2016', 'Clinton':48.2 , 'Trump':46.1}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D = D.dropna(subset=['Date'])
  

D['total']=D[parties].sum(axis=1)

D['decided']=D['total']

parties = ['Clinton', 'Trump']
D[parties] = D[parties].div(D['decided'], axis=0)*100

D = D.drop(["decided","total"], axis=1)

D.to_csv('US/old/poll3.csv', index=False)
  
