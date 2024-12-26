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
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','Lab','Con','Reform','Lib Dem','Green']
parties = ['Lab','Con','Reform','Lib Dem','Green']
d = {}
for i in range(1):
  # i=j+1
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Pollster", "Client", "Area", "Others", "Lead", "Sample size"], axis=1)
  d[i].columns = headers
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Lab'] != d[i]['Green']]

D = pd.concat(d.values(), ignore_index=True)

for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
  
D.drop(D.index[[-2]],inplace=True)
D = D.reset_index(drop=True)
D.loc[len(D.index)-1,['Date']] = '4 July 2024'
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


D.to_csv('UK/general_polling/poll.csv', index=False)


govt = ['Lab','Green']
opp = ['Reform','Con']

D[parties] = D[parties].astype(float)
D['Left (Lab+Green)'] = D[govt].sum(axis=1)
D['Right (Con+Ref)'] = D[opp].sum(axis=1)

D = D.drop(govt, axis=1)
D = D.drop(opp, axis=1)
parties = ['Left (Lab+Green)','Lib Dem','Right (Con+Ref)']
D['total']=D[parties].sum(axis=1)
D[parties] = D[parties].div(D['total'], axis=0)
D = D.drop(["total"], axis=1)
D = D[['Date','Left (Lab+Green)','Lib Dem','Right (Con+Ref)']]
D.to_csv('UK/general_polling/poll_bloc.csv', index=False)
