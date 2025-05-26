import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Next_Northern_Ireland_Assembly_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )


headers = ['Date','1','2','3','SF','DUP','APNI','UUP','SDLP','TUV','Green','Aontú','PBP','Other','4']
parties = ['SF','DUP','APNI','UUP','SDLP','TUV','Green','Aontú','PBP','Other']
drops = ['1','2','3','4']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[0])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]=d[i][~d[i].Date.str.contains("4 Jul 2024")]
  d[i]=d[i][~d[i].Date.str.contains("18 May 2023")]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  
  
  
D = pd.concat(d.values(), ignore_index=True)

for z in parties:
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  D[z] = D[z].str.split('%').str[0]
  D[z] = pd.to_numeric(D[z], errors='coerce')
  D = D.dropna(subset=['TUV'])




D.to_csv('UK/Subnational/Northern Ireland/poll.csv', index=False)



D = pd.concat(d.values(), ignore_index=True)


for z in parties:
  D[z] = [p.sub('', x) for x in D[z].astype(str)]
  for x in range(len(d[i]['Date'])):
    D[z][x] = str(D[z][x])
    if len(D[z][x].split('%'))>2:
      D[z][x] = D[z][x].split('%')[2]
    elif len(D[z][x].split('%'))>1:
      D[z][x] = D[z][x].split('%')[1]
    else:
      pass
  D[z] = pd.to_numeric(D[z], errors='coerce')
D = D.dropna(subset=['TUV'])



D.to_csv('UK/Subnational/Northern Ireland/poll2.csv', index=False)
