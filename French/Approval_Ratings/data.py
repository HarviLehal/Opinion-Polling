import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import numpy as np

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_on_the_Emmanuel_Macron_presidency"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
print(df[0])

# MACRON AND BORNE

Macron = [0,2,6,7,8,9,10,11]
Borne = [0,2,3,4,5,6,10,11]
dfm0=pd.DataFrame(df[0])
dfb=pd.DataFrame(df[0])
dfm0.drop(dfm0.columns[Macron], axis=1, inplace=True)
dfb.drop(dfb.columns[Borne], axis=1, inplace=True)
headersM = ['Date', 'Macron Approve', 'Macron Disapprove', 'Macron Unsure']
headersB = ['Date', 'Borne Approve', 'Borne Disapprove', 'Borne Unsure']
partiesM = ['Macron Approve', 'Macron Disapprove', 'Macron Unsure']
partiesB = ['Borne Approve', 'Borne Disapprove', 'Borne Unsure']

dfm0.columns = headersM
dfb.columns = headersB
dfs0 = [dfm0,dfb]

for z in dfs0:
  z['Date'] = [x.strip()[-12:] for x in z['Date']]
  z['Date'] = [x.replace('–','') for x in z['Date']]
  z['Date'] = [x.replace('-','') for x in z['Date']]

  z.Date = z.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
for x in partiesM:
  dfm0[x] = [y.replace('~','') for y in dfm0[x]]
  dfm0[x] = dfm0[x].str.rstrip('%').astype('float') / 100.0

for x in partiesB:
  dfb[x] = [y.replace('~','') for y in dfb[x]]
  dfb[x] = dfb[x].str.rstrip('%').astype('float') / 100.0
print(dfs0)
# MACRON AND CASTEX

Macron = [0,2,6,7,8,9,10,11]
Castex = [0,2,3,4,5,6,10,11]
dfm1=pd.DataFrame(df[1])
dfc=pd.DataFrame(df[1])
dfm1.drop(dfm1.columns[Macron], axis=1, inplace=True)
dfc.drop(dfc.columns[Castex], axis=1, inplace=True)
headersC = ['Date', 'Castex Approve', 'Castex Disapprove', 'Castex Unsure']
partiesC = ['Castex Approve', 'Castex Disapprove', 'Castex Unsure']
dfm1.columns = headersM
dfc.columns = headersC
dfs1 = [dfm1,dfc]

for z in dfs1:
  z['Date'] = [x.strip()[-12:] for x in z['Date']]
  z['Date'] = [x.replace('–','') for x in z['Date']]
  z['Date'] = [x.replace('-','') for x in z['Date']]
  z.Date = z.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
for x in partiesM:
  dfm1[x] = [y.replace('~','') for y in dfm1[x]]
  dfm1[x] = dfm1[x].str.rstrip('%').astype('float') / 100.0

for x in partiesC:
  dfc[x] = [y.replace('~','') for y in dfc[x]]
  dfc[x] = dfc[x].str.rstrip('%').astype('float') / 100.0
print(dfs1)

# MACRON AND Philippe

Macron = [0,2,6,7,8,9,10,11]
Philippe = [0,2,3,4,5,6,10,11]
dfm2=pd.DataFrame(df[2])
dfp=pd.DataFrame(df[2])
dfm2.drop(dfm2.columns[Macron], axis=1, inplace=True)
dfp.drop(dfp.columns[Philippe], axis=1, inplace=True)
headersP = ['Date', 'Philippe Approve', 'Philippe Disapprove', 'Philippe Unsure']
partiesP = ['Philippe Approve', 'Philippe Disapprove', 'Philippe Unsure']
dfm2.columns = headersM
dfp.columns = headersP
dfs2 = [dfm2,dfp]

for z in dfs2:
  z['Date'] = [x.strip()[-12:] for x in z['Date']]
  z['Date'] = [x.replace('–','') for x in z['Date']]
  z['Date'] = [x.replace('-','') for x in z['Date']]
  z.Date = z.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  
for x in partiesM:
  dfm2[x] = [y.replace('~','') for y in dfm2[x]]
  dfm2[x] = dfm2[x].str.rstrip('%').astype('float') / 100.0

for x in partiesP:
  dfp[x] = [y.replace('~','') for y in dfp[x]]
  dfp[x] = dfp[x].str.rstrip('%').astype('float') / 100.0
print(dfs2)




# SAVE

macron = pd.concat([dfm0,dfm1,dfm2])
borne = dfb
castex = dfc
philippe = dfp

macron.to_csv('French/Approval_Ratings/macron.csv', index=False)
borne.to_csv('French/Approval_Ratings/borne.csv', index=False)
castex.to_csv('French/Approval_Ratings/castex.csv', index=False)
philippe.to_csv('French/Approval_Ratings/philippe.csv', index=False)
