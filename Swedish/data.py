import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_Swedish_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
headers = ['Polling firm', 'Date', 'Sample size', 'V', 'S', 'MP', 'C', 'L', 'M', 'KD', 'SD', 'Other', 'Lead1', 'Opp', 'Gov', 'Lead2', 'OppSeat', 'GovSeat', 'Lead3']
parties = ['V', 'S', 'MP', 'C', 'L', 'M', 'KD', 'SD']

# POLL OF PARTIES

d = {}
for i in range(2):
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(["Polling firm", "Sample size", "Other", "Lead1", "Lead2", "Lead3", "Opp", "Gov", "OppSeat","GovSeat"], axis=1)
  if i == 0:
    d[i].drop(d[i].index[[-1]],inplace=True)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['S'] != d[i]['V']]

for i in range(1):
  d[i].drop(d[i].index[[-1]],inplace=True)

D = pd.concat(d.values(), ignore_index=True)
D.loc[len(D.index)-1,['Date']] = '11 Sep 2022'
D.Date = D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
D.to_csv('Swedish/poll.csv', index=False)

# SEAT PROJECTION OF COALITIONS

e = {}
for i in range(2):
  e[i]=pd.DataFrame(df[i])
  e[i].columns = headers
  e[i]=e[i].drop(['Polling firm', 'Sample size', 'V', 'S', 'MP', 'C', 'L', 'M', 'KD', 'SD', 'Other', 'Lead1', 'Opp', 'Gov', 'Lead2', 'Lead3'], axis=1)
  if i == 0:
    e[i].drop(e[i].index[[-1]],inplace=True)
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i]['Date'].str.split('-').str[1], inplace=True)
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date2'] = [x+ str(2023-i) for x in e[i]['Date2'].astype(str)]
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

for i in range(1):
  e[i].drop(e[i].index[[-1]],inplace=True)

E = pd.concat(e.values(), ignore_index=True)
E.loc[len(E.index)-1,['Date']] = '11 Sep 2022'
E.Date = E.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
E.columns = ['Date','Opposition','Government']
E.to_csv('Swedish/seats.csv', index=False)

# POLL PROJECTION OF COALITIONS

f = {}
for i in range(2):
  f[i]=pd.DataFrame(df[i])
  f[i].columns = headers
  f[i]=f[i].drop(['Polling firm', 'Sample size', 'V', 'S', 'MP', 'C', 'L', 'M', 'KD', 'SD', 'Other', 'Lead1', 'Lead2', 'OppSeat', 'GovSeat', 'Lead3'], axis=1)
  if i == 0:
    e[i].drop(e[i].index[[-1]],inplace=True)
  f[i]['Date2'] = f[i]['Date'].str.split('–').str[1]
  f[i].Date2.fillna(f[i]['Date'].str.split('-').str[1], inplace=True)
  f[i].Date2.fillna(f[i].Date, inplace=True)
  f[i]['Date2'] = [x+ str(2023-i) for x in f[i]['Date2'].astype(str)]
  f[i]['Date'] = f[i]['Date2']
  f[i] = f[i].drop(['Date2'], axis=1)
  f[i].Date=f[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

for i in range(1):
  f[i].drop(f[i].index[[-1]],inplace=True)

F = pd.concat(f.values(), ignore_index=True)
F.loc[len(F.index)-1,['Date']] = '11 Sep 2022'
F.Date = F.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
F.columns = ['Date','Opposition','Government']
F.to_csv('Swedish/coalition.csv', index=False)
