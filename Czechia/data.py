import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Czech_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','ODS','KDU-CSL','TOP09','ANO','STAN','Piráti','SPD','1','2','Přísaha','3','SOCDEM','KSČM','Zelení','PRO']
parties = ['ODS','KDU-CSL','TOP09','ANO','STAN','Piráti','SPD','Přísaha','SOCDEM','KSČM','Zelení','PRO']
drops = ['1','2','3']
d = {}
for i in range(1):
  # i=j+1
  d[i]=pd.DataFrame(df[i+2])
  d[i]=d[i].drop(["Polling firm", "Sample size", "Gov.","Opp.", "Others", "Lead"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]=d[i][d[i]['Date'] != '7–8 Jun 2024']
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['ANO'] != d[i]['Zelení']]

D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].astype('float')

D = D.dropna(subset=['ANO'])

SPOLU = ['ODS','KDU-CSL','TOP09']


D['Spolu']=D[SPOLU].sum(axis=1)




D = D.drop(SPOLU, axis=1)

D= D[['Date','Spolu','ANO','STAN','Piráti','SPD','Přísaha','SOCDEM','KSČM','Zelení','PRO']]

D.loc[D['Spolu'] > 50, 'Spolu'] = D['Spolu']/3


D.to_csv('Czechia/poll.csv', index=False)
