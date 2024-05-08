import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_2019_United_Kingdom_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')
p2 = re.compile(r'\*')


headers = ['Date','Con','Lab','SNP','Lib Dem','DUP','Plaid Cymru','SDLP','Green','APNI','Alba','Reclaim','WPB','Reform UK','Ind.','Sinn Féin']
parties = ['Con','Lab','SNP','Lib Dem','DUP','Plaid Cymru','SDLP','Green','APNI','Alba','Reclaim','WPB','Reform UK','Ind.','Sinn Féin']
d = {}
for i in range(1):
  # i=j+1
  d[i]=pd.DataFrame(df[-1])
  d[i]=d[i].drop(["Event", "Working majority", "Spkr", "Working majority", "Vacant","SF","Unnamed: 18","Unnamed: 21"], axis=1)
  d[i].columns = headers
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [p2.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Con'] != d[i]['Green']]



D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype('float')

D = D.drop_duplicates(subset=['Date'], keep='last')

D.to_csv('UK/Seats/poll2.csv', index=False)




headers = ["Date","Working Majority"]
parties = ["Working Majority"]
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-1])
  d[i]=d[i][["Date","Working majority"]]
  d[i].columns = headers
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [p2.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBC',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('TBA',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z]]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x))
  
D = pd.concat(d.values(), ignore_index=True)
for z in parties:
  D[z] = D[z].astype('float')
D=D.dropna(subset=['Working Majority'])

D = D.drop_duplicates(subset=['Date'], keep='last')

D.to_csv('UK/Seats/poll3.csv', index=False)

