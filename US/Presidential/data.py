import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Nationwide_opinion_polling_for_the_2024_United_States_presidential_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date', 'Harris', 'Trump', 'Other']
parties = ['Harris', 'Trump', 'Other']
d = {}
for i in range(1):
  # i=j+1
  d[i]=pd.DataFrame(df[i+1])
  d[i]=d[i].drop(["Poll source","Sample size[b]","Margin of error"], axis=1)
  d[i].columns = headers
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[0]
  d[i]['Date2'] = d[i]['Date2'].str.split(',').str[0]
  # d[i]['Date2'] = (d[i]['Date2']+' ' + d[i]['Date'].str.split(',')[1]).astype(str)
  # d[i]['Date2'] = [x.split(',')[1] if len(x.split(',')) > 0 else '' for x in d[i]['Date'].astype(str)]
  d[i]['Date2'] = (d[i]['Date2']+[x.split(',')[1] if len(x.split(',')) > 0 else '' for x in d[i]['Date'].astype(str)]).astype(str)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date = d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Harris'] != d[i]['Other']]

D = pd.concat(d.values(), ignore_index=True)

for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
  
new_row = pd.DataFrame({'Date': '03 November 2020', 'Harris':51.31 , 'Trump':46.85 , 'Other':1.84}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D = D.dropna(subset=['Date'])


D.to_csv('US/Presidential/poll.csv', index=False)


D['Other'].fillna(0, inplace=True)
D['total']=D[parties].sum(axis=1)

D['decided']=D['total']-D['Other']

parties = ['Harris', 'Trump']
D[parties] = D[parties].div(D['decided'], axis=0)*100

D = D.drop(["decided","total","Other"], axis=1)

D.to_csv('US/Presidential/poll2.csv', index=False)
