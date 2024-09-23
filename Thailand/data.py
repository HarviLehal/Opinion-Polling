import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re
from io import StringIO

# 
# wikiurl="https://en.wikipedia.org/wiki/2023_Thai_general_election"
# table_class="wikitable sortable jquery-tablesorter"
# response=requests.get(wikiurl)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'html.parser')
# tables = soup.find_all('table',class_="wikitable")
# df=pd.read_html(str(tables))
# p = re.compile(r'\[[a-z]+\]'  )
# 
# headers = ['Date','1','2','PPRP','PTP','MFP','Dem','BJT','TLP','3','4','5','TST','UTN','UNDECIDED','7','8']
# parties = ['PPRP','PTP','MFP','Dem','BJT','TLP','TST','UTN','UNDECIDED']
# drops = ['1','2','3','4','5','7','8']
# 
# d = {}
# for i in range(1):
#   d[i]=pd.DataFrame(df[5])
#   d[i].columns = headers
#   d[i]=d[i].drop(drops, axis=1)
#   d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
#   d[i].Date2.fillna(d[i].Date, inplace=True)
#   d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
#   d[i]['Date'] = d[i]['Date2']
#   d[i] = d[i].drop(['Date2'], axis=1)
#   d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
#   d[i] = d[i][d[i]['PTP'] != d[i]['TST']]
#   for z in parties:
#     d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
#     d[i][z] = d[i][z].str.split(' ').str[0]
#     d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
#     d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
#     d[i][z] = [x.replace('Did',str(np.NaN)) for x in d[i][z].astype(str)]
# 
# D = pd.concat(d.values(), ignore_index=True)
# D = D.replace(r'^\s*$', np.NaN, regex=True)
# for z in parties:
#   D[z] = D[z].astype(str)
#   D[z] = D[z].str.strip('%')
#   D[z] = D[z].astype('float')
# 
# 
# new_row = pd.DataFrame({'Date': '14 May 2023', 'PPRP':1.41,'PTP':28.84,'MFP':37.99,'Dem':2.43,'BJT':2.99,'TLP':0.92,'TST':0.9,'UTN':12.54}, index=[0])
# D = pd.concat([new_row,D]).reset_index(drop=True)
# D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
# 
# 
# D['UNDECIDED'].fillna(0, inplace=True)
# D['total']=D[parties].sum(axis=1)
# 
# D['decided']=D['total']-D['UNDECIDED']
# D['ratio'] = D['total'].div(D['decided'], axis=0)
# 
# parties = ['PPRP','PTP','MFP','Dem','BJT','TLP','TST','UTN']
# D[parties] = D[parties].multiply(D['ratio'],axis=0)
# 
# D = D.drop(["decided","total","UNDECIDED",'ratio'], axis=1)
# 
# D.to_csv('Thailand/poll.csv', index=False)
# 
# 
# 
# 
# 
# 
# 






















wikiurl="https://en.wikipedia.org/wiki/Next_Thai_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['Date','1','2','MFP','PTP','UTN','BJT','Dem','PPRP','UNDECIDED','3','4']
parties = ['MFP','PTP','UTN','BJT','Dem','PPRP','UNDECIDED']
drops = ['1','2','3','4']

d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-3])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['PTP'] != d[i]['BJT']]
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('Did',str(np.NaN)) for x in d[i][z].astype(str)]

D = pd.concat(d.values(), ignore_index=True)
D = D.replace(r'^\s*$', np.NaN, regex=True)
for z in parties:
  D[z] = D[z].astype(str)
  D[z] = D[z].str.strip('%')
  D[z] = D[z].astype('float')
  
  
  
D['UNDECIDED'].fillna(0, inplace=True)
D['total']=D[parties].sum(axis=1)

D['decided']=D['total']-D['UNDECIDED']
D['ratio'] = D['total'].div(D['decided'], axis=0)

parties = ['MFP','PTP','UTN','BJT','Dem','PPRP']
D[parties] = D[parties].multiply(D['ratio'],axis=0)

D = D.drop(["decided","total","UNDECIDED",'ratio'], axis=1)

D.to_csv('Thailand/poll_new.csv', index=False)
