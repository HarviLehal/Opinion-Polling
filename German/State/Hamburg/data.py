import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2025_Hamburg_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )


headers = ['1','Date','2','SPD','Grüne','CDU','Linke','AfD','FDP','Volt','BSW','Other','3']
parties = ['SPD','Grüne','CDU','Linke','AfD','FDP','Volt','BSW','Other']
drops = ['1','2','3']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[0])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i] = d[i].dropna(subset=['Date'])
  d[i]=d[i][~d[i].Date.str.contains("9 Jun 2024")]
  d[i]=d[i][~d[i].Date.str.contains("26 Sep 2021")]
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
  d[i] = d[i].dropna(subset=['SPD'])


D = pd.concat(d.values(), ignore_index=True)



  

D.to_csv('German/State/Hamburg/poll.csv', index=False)
