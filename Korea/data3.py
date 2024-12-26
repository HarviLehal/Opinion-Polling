import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_on_the_Yoon_Suk_Yeol_presidency"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
p = re.compile(r'\[[a-z]+\]')
df=pd.read_html(str(tables))

headers = ['Date','Approve','Disapprove','Undecided']
parties = ['Approve','Disapprove','Undecided']
d = {}

for i in range(3):
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["Sample size","Polling firm",'Margin of error', "Net"], axis=1)
  d[i].columns = headers

  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[0], inplace=True)
  if d[i]['Date2'].str.contains('Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec').any():
    pass
  else:
    d[i]['Date2'] = [x+' '+ d[i]['Date'].str[:3] for x in d[i]['Date2'].astype(str)]
  d[i]['Date2'] = [x+' '+ str( 2024-i) for x in d[i]['Date2'].astype(str)]
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

D.to_csv('Korea/approval.csv', index=False)


D['total']=D[parties].sum(axis=1)
D['decided']=D['total']-D['Undecided']

print(D)
parties = ['Approve','Disapprove']
D[parties] = D[parties].div(D['decided'], axis=0)*100

D = D.drop(["decided","total","Undecided"], axis=1)
D['Net Approval']=D['Approve']-D['Disapprove']
D = D.drop(["Approve","Disapprove"], axis=1)
D.to_csv('Korea/approval2.csv', index=False)
