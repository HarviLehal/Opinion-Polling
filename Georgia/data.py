import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/2024_Georgian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')


headers=['Date','1', 'SOURCE','GD1','GD2','UNM1','UNM2','UNM3','FG1','FG2','C4C1','C4C2','C4C3','C4C4','SG1','SG2','SG3','SG4','Girchi','GLP','APG1','APG2','APG3','2','Other','3','4']
parties = ['GD1','GD2','UNM1','UNM2','UNM3','FG1','FG2','C4C1','C4C2','C4C3','C4C4','SG1','SG2','SG3','SG4','Girchi','GLP','APG1','APG2','APG3','Other']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[-2])
  d[i].loc[len(d[i].index)-1,['Date']] = '31 October 2020'
  d[i].columns = headers
  d[i] = d[i][~d[i]['SOURCE'].str.contains('GORBI' ,na=False)]
  d[i]=d[i].drop(["SOURCE","1","2","3","4"], axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  # d[i]['Date2'] = [x+ str(2023-i) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z]]
    d[i][z] = [x.replace('>','') for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('<','') for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
D = pd.concat(d.values(), ignore_index=True)
D = D.fillna(0)

GD = ['GD1','GD2']
UNM = ['UNM1','UNM2','UNM3']
FG = ['FG1','FG2']
C4C = ['C4C1','C4C2','C4C3','C4C4']
SG = ['SG1','SG2','SG3','SG4']
APG = ['APG1','APG2','APG3']
D['GD']=np.where(D['GD1']==D['GD2'],D['GD1'],D[GD].sum(axis=1))
D['UNM']=np.where((D['UNM1']==D['UNM2']) & (D['UNM1']==D['UNM3']),D['UNM1'], np.where(D['UNM1']==D['UNM2'],D['UNM1']+D['UNM3'],D[UNM].sum(axis=1)))
D['FG']=np.where(D['FG1']==D['FG2'],D['FG1'],D[FG].sum(axis=1))
D['C4C']=np.where((D['C4C1']==D['C4C2']) & (D['C4C1']==D['C4C3']) & (D['C4C1']==D['C4C4']),D['C4C1'], np.where((D['C4C1']==D['C4C2']) & (D['C4C1']==D['C4C3']),D['C4C1'],np.where(D['C4C1']==D['C4C2'],D['C4C1']+D['C4C3'], D[C4C].sum(axis=1))))
D['SG']=np.where((D['SG1']==D['SG2']) & (D['SG1']==D['SG3']) & (D['SG1']==D['SG4']),D['SG1'], np.where((D['SG1']==D['SG2']) & (D['SG1']==D['SG3']),D['SG1']+D['SG4'],np.where(D['SG1']==D['SG2'],D['SG1']+D['SG3'], D[SG].sum(axis=1))))
D['APG']=np.where((D['APG1']==D['APG2']) & (D['APG1']==D['APG3']),D['APG1'], np.where(D['APG1']==D['APG2'],D['APG1']+D['APG3'],D[APG].sum(axis=1)))

D = D.drop(GD, axis=1)
D = D.drop(UNM, axis=1)
D = D.drop(FG, axis=1)
D = D.drop(C4C, axis=1)
D = D.drop(SG, axis=1)
D = D.drop(APG, axis=1)


D=D[['Date','GD','UNM','FG','C4C','SG','Girchi','GLP','APG','Other']]
D.replace(0, np.nan, inplace=True)


G=53.064
U=9.847
F=8.222
C=11.176
S=8.998
GI=3.215
GL=0.752
A=2.527
O=100-G-U-F-C-S-GI-GL-A

new_row = pd.DataFrame({'Date':'26 October 2024','GD':G,'UNM':U,'FG':F,'C4C':C,'SG':S,'Girchi':GI,'GLP':GL,'APG':A,'Other':O}, index=[0])
D = pd.concat([new_row,D]).reset_index(drop=True)
D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

D.to_csv('Georgia/poll.csv', index=False)
