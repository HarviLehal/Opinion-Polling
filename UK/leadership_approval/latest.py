import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','Keir Starmer','Rishi Sunak','Unsure']
parties = ['Keir Starmer','Rishi Sunak','Unsure']
d = {}
for i in range(4):
  j = i + 27
  d[i]=pd.DataFrame(df[j])
  d[i]=d[i].drop(["Pollster/client","Area","Lead","Sample size"], axis=1)
  d[i].columns = headers
  for z in headers:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–','-') for x in d[i][z]]
    d[i][z] = [x.replace('TBC','-') for x in d[i][z]]
    d[i][z] = [x.replace('?','-') for x in d[i][z]]
    
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
D = pd.concat(d.values(), ignore_index=True)
E = pd.concat([d[0],d[1]], ignore_index=True)
E.drop(E.index[[-1,-2,-3,-4,-5]],inplace=True)
for z in parties:
  E[z] = E[z].str.rstrip('%').astype('float')
parties = ['Keir Starmer','Rishi Sunak']
E[parties] = E[parties].div(E[parties].sum(axis=1), axis=0)
E = E.drop('Unsure', axis=1)

D.to_csv('UK/leadership_approval/latest.csv', index=False)
E.to_csv('UK/leadership_approval/latest2023.csv', index=False)
