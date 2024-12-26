import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_Japanese_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','PM','Approve','Disapprove','Undecided']
parties = ['Approve','Disapprove','Undecided']
d = {}

for i in range(4):
  d[i]=pd.DataFrame(df[-4+i])
  d[i]=d[i].drop(["Sample size","Polling firm", "Lead"], axis=1)
  d[i].columns = headers
  d[i] = d[i][d[i]['PM'] != 'Fumio Kishida']
  d[i]=d[i].drop(["PM"], axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x+ str(2024-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Approve'] != d[i]['Undecided']]
  # d[i] = d[i][d[i]['Approve'] == d[i]['Undecided']]
  for z in parties:
    d[i][z] = d[i][z].astype('string')
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]



D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Approve'])

D.to_csv('Japan/approval/poll_approval.csv', index=False)


D['total']=D[parties].sum(axis=1)
D['decided']=D['total']-D['Undecided']

print(D)
parties = ['Approve','Disapprove']
D[parties] = D[parties].div(D['decided'], axis=0)*100

D = D.drop(["decided","total","Undecided"], axis=1)

D.to_csv('Japan/approval/poll_approval2.csv', index=False)

D['Net Approval']=D['Approve']-D['Disapprove']
D = D.drop(["Approve","Disapprove"], axis=1)
D.to_csv('Japan/approval/poll_approval_net2.csv', index=False)


D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = pd.to_numeric(D[z], errors='coerce')
D=D.dropna(subset=['Approve'])
D['Net Approval']=D['Approve']-D['Disapprove']
D = D.drop(["Approve","Disapprove"], axis=1)

D.to_csv('Japan/approval/poll_approval_net.csv', index=False)
