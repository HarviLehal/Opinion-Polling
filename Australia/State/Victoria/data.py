import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2026_Victorian_state_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers=['Date', 'Firm','Sample', 'Labor', 'LNP','LNP2', 'Green', 'Other', 'Labor2', 'Coalition2']
parties = ['Labor', 'LNP','LNP2', 'Green', 'Other', 'Labor2', 'Coalition2']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i].columns = headers
  d[i]=d[i].drop(["Firm","Sample"], axis=1)
  d[0].loc[len(d[0].index)-4,['Date']] = '26 November 2022'
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Labor'] != d[i]['Green']]
  for z in parties:
    d[i][z] = d[i][z].str.split('%').str[0]
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = d[i][z].astype('float')


D = pd.concat(d.values(), ignore_index=True)
D.drop(D.index[[-1]],inplace=True)

D['LNP']=np.where(D['LNP']==D['LNP2'],D['LNP'],D['LNP']+D['LNP2'])
D=D.drop(["LNP2"], axis=1)
PP = ['Labor2', 'Coalition2']
E = D.drop(PP, axis=1)
E.to_csv('Australia/State/Victoria/poll.csv', index=False)


parties2 = ['Labor', 'LNP', 'Green', 'Other']
D = D.drop(parties2, axis=1)
headers = ['Date', 'Labor', 'LNP']
D.columns = headers
D.to_csv('Australia/State/Victoria/poll2.csv', index=False)
