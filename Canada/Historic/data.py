import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2021_Canadian_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  parties = heads[3:-5]
  d[i] = d[i].drop(d[i].columns[[0,2,-1,-2,-3,-4,-5]],axis = 1)
  d[i].rename(columns={ d[i].columns[0]: "Date" }, inplace = True)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['CPC'])
  
D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[0]],inplace=True)
D.to_csv('Canada/Historic/poll_21.csv', index=False)


wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2019_Canadian_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  parties = heads[3:-5]
  d[i] = d[i].drop(d[i].columns[[0,2,-1,-2,-3,-4,-5]],axis = 1)
  d[i].rename(columns={ d[i].columns[0]: "Date" }, inplace = True)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['CPC'])
  
D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[0]],inplace=True)
D.to_csv('Canada/Historic/poll_19.csv', index=False)


wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2015_Canadian_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  parties = heads[3:-4]
  d[i] = d[i].drop(d[i].columns[[0,2,-1,-2,-3,-4]],axis = 1)
  d[i].rename(columns={ d[i].columns[0]: "Date" }, inplace = True)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['CPC'])
  
D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[0]],inplace=True)
D.to_csv('Canada/Historic/poll_15.csv', index=False)


wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2011_Canadian_federal_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i])
  heads = []
  for j in range(len(df[i].columns)):
    heads.append(df[i].columns[j][0])
  d[i]=pd.DataFrame(df[i])
  d[i].columns = heads
  if i ==0:
    parties = heads[3:-3]
    d[i] = d[i].drop(d[i].columns[[0,2,-1,-2,-3]],axis = 1)
  else:
    parties = heads[3:-1]
    d[i] = d[i].drop(d[i].columns[[0,2,-1]],axis = 1)
    
  d[i].rename(columns={ d[i].columns[0]: "Date" }, inplace = True)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Date'])
  d[i] = d[i].dropna(subset=['CPC'])
  
D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[0]],inplace=True)
D.to_csv('Canada/Historic/poll_11.csv', index=False)



