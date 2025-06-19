import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2026_Berlin_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','CDU','SPD','Grüne','Linke','AfD','FDP','BSW','Others']
parties = ['CDU','SPD','Grüne','Linke','AfD','FDP','BSW','Others']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[0])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Lead"], axis=1)
  d[i].columns = headers
  d[i]=d[i][~d[i].Date.str.contains("23 Feb 2025")]
  d[i]=d[i][~d[i].Date.str.contains("9 Jun 2024")]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['CDU'] != d[i]['FDP']]

D = pd.concat(d.values(), ignore_index=True)

parties = ['CDU','SPD','Grüne','Linke','AfD','FDP','BSW','Others']
# parties = ['SPD','Union','Grüne','FDP','AfD','Linke']
for z in parties:
    D[z] = [p.sub('', x) for x in D[z].astype(str)]
    D[z] = [x.replace('–',str(np.nan)) for x in D[z].astype(str)]
    D[z] = [x.replace('—',str(np.nan)) for x in D[z].astype(str)]
D[parties] = D[parties].astype(float)

D.to_csv('German/State/Berlin/poll.csv', index=False)

