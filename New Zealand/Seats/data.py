import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re


wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_New_Zealand_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','Nat','Lab','Green','ACT','NZF','TPM','TOP']
parties = ['Nat','Lab','Green','ACT','NZF','TPM']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i]=d[i].drop(["Likely government formation"], axis=1)
  d[i].columns = headers
  d[i]=d[i].drop(["TOP"], axis=1)
  d[i]['Date'] = d[i]['Date'].str.split(']').str[1]
  d[i]['Date'] = [x.replace(' poll','') for x in d[i]['Date']]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Lab'] != d[i]['ACT']]
  for z in parties:
    d[i][z] = d[i][z].astype('str')
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('*','') for x in d[i][z]]


  


D = pd.concat(d.values(), ignore_index=True)
D=D.dropna(subset=['Date'])
D[parties] = D[parties].astype(float)
D=D.dropna(subset=['Lab'])

for z in parties:
  D[z] = D[z].astype('float')
D.to_csv('New Zealand/Seats/poll.csv', index=False)

parties = ['Lab','Nat','Green','ACT','TPM']

Gov=['Lab', 'Green', 'TPM']
Opp=['Nat', 'ACT', 'NZF']
D = D.dropna(subset=['Green'])
D[parties] = D[parties].astype(float)

D['Lab + Green + TPM'] = D[Gov].sum(axis=1)
D['Nat + ACT + NZF'] = D[Opp].sum(axis=1)
# D['Other'] = 100-D['Lab + Green']-D['Nat + ACT']
D = D.drop(parties, axis=1)
D = D[['Date','Lab + Green + TPM','Nat + ACT + NZF']]
D.to_csv('New Zealand/Seats/poll2.csv', index=False)
