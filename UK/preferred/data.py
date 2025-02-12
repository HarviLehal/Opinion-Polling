import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )


headers = ['Date','1','2','Starmer','Sunak','Farage','3','4','5','6']
parties = ['Starmer','Sunak','Farage']
drops = ['1','2','3','4','5','6']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-3])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.strip('%')
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')

  d[i] = d[i].dropna(subset=['Starmer'])


D = pd.concat(d.values(), ignore_index=True)
D = D.loc[~D.index.isin(D.dropna(subset=['Farage']).index)]
D=D.drop(['Farage'], axis=1)
parties = ['Starmer','Sunak']
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)
D = D.drop(["total"], axis=1)


split_date = '2 November 2024'
split_date=dateparser.parse(split_date)
c={}
c[0]=D[D["Date"] > split_date]
c[0].rename(columns={"Sunak": 'Badenoch'}, inplace=True)
c[1]=D[D["Date"] < split_date]
D = pd.concat(c.values(), ignore_index=True)


D = D.loc[~D.index.isin(D[D["Starmer"]>0.9999].index)]



  

D.to_csv('UK/preferred/poll.csv', index=False)
