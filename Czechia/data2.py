import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://cs.wikipedia.org/wiki/P%C5%99edvolebn%C3%AD_pr%C5%AFzkumy_k_volb%C3%A1m_do_Poslaneck%C3%A9_sn%C4%9Bmovny_Parlamentu_%C4%8Cesk%C3%A9_republiky_2025"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')
p = re.compile(r'\[[a-z]+\]')

headers = ['Date','ANO','ODS','TOP09','KDU-CSL','Piráti','STAN','SPD','Trikolora','Svobodní','PRO','AUTO','Stačilo!','SOCDEM','PŘÍSAHA','Zelení','ostatní']
parties = ['ANO','ODS','TOP09','KDU-CSL','Piráti','STAN','SPD','Trikolora','Svobodní','PRO','AUTO','Stačilo!','SOCDEM','PŘÍSAHA','Zelení','ostatní']
# drops = ['1','2']
d = {}
for i in range(1):
  # i=j+1
  d[i]=pd.DataFrame(df[i])
  d[i]=d[i].drop(["agentura (zdroj)"], axis=1)
  d[i].columns = headers
  # d[i]=d[i].drop(drops, axis=1)
  d[i]=d[i][d[i]['Date'] != '7.–8.6.2024']
  for z in parties:
    d[i][z] = d[i][z].astype(str)
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z]]
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  # d[i]['Date'] = [x.replace('.','/' for x in d[i]['Date']]
  d[i].loc[len(d[i].index),['Date']] = '09/10/2021'
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first','DATE_ORDER': 'DMY'}))
  d[i] = d[i][d[i]['ANO'] != d[i]['Zelení']]

D = pd.concat(d.values(), ignore_index=True)
# for z in parties:
# D[z] = D[z].astype(str)
# D[z] = D[z].astype('float')

D = D.dropna(subset=['ANO'])

SPOLU = ['ODS','KDU-CSL','TOP09']


# D['SPOLU']=D[SPOLU].sum(axis=1)
for z in SPOLU:
  D[z]=np.where(np.isnan(D[z])==True,0,D[z])

D['SPOLU']=np.where(D['ODS']==D['TOP09'], D['ODS'], D[SPOLU].sum(axis=1))
D = D.drop(SPOLU, axis=1)


split_date = '26 Mar 2025'
split_date=dateparser.parse(split_date)
c={}
c[0]=D[(pd.to_datetime(D["Date"]) > split_date)]
c[1]=D[(pd.to_datetime(D["Date"]) < split_date)]

vs = ['SPD','Trikolora','Svobodní','PRO']
for z in vs:
  c[0][z]=np.where(np.isnan(c[0][z])==True,0,c[0][z])

c[0]['SPD']=np.where(c[0]['SPD']==c[0]['PRO'],c[0]['SPD'],c[0][vs].sum(axis=1))
vs = ['Trikolora','Svobodní','PRO']
c[0] = c[0].drop(vs, axis=1)

C = pd.concat(c.values(), ignore_index=True)

D = C

D= D[['Date','SPOLU','ANO','STAN','Piráti','SPD','Trikolora','Svobodní','PRO','PŘÍSAHA','AUTO','SOCDEM','Stačilo!','Zelení']]

# D.loc[D['SPOLU'] > 50, 'SPOLU'] = D['SPOLU']/3


D['STAN']=np.where(D['Piráti']==D['STAN'], np.nan, D['STAN'])
D.loc[len(D.index)-1,['STAN']] = 15.62
D = D.dropna(subset=['STAN'])


D.to_csv('Czechia/poll.csv', index=False)
