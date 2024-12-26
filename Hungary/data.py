import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_Hungarian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

headers = ['Date','1','2','Fidesz','DK','MSZP','Zöldek','Momentum','Jobbik','LMP','3','MHM','MKKP','4','5','TISZA','Other','6']
parties = ['Fidesz','DK','MSZP','Zöldek','Momentum','Jobbik','LMP','MHM','MKKP','TISZA','Other']
drops = ['1','2','3','4','5','6']
d = {}
for i in range(1):
  d[i]=pd.DataFrame(df[1])
  d[i].columns = headers
  d[i]=d[i].drop(drops, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i]['Date'].str.split('-').str[1], inplace=True)
  d[i].Date2.fillna(d[i].Date, inplace=True)
  d[i]['Date2'] = [x for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i]=d[i][~d[i].Date.str.contains("9 Jun 2024")]
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = d[i][z].str.split(' ').str[0]
    d[i][z] = [x.replace('–',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('-',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('?',str(np.nan)) for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Fidesz'])

D = pd.concat(d.values(), ignore_index=True)

split_date1 = '28 March 2024'
split_date1=dateparser.parse(split_date1)

split_date2 = '19 September 2024'
split_dat2=dateparser.parse(split_date2)



c={}
c[0]=D[D["Date"]<split_date1]
c[1]=D[(D["Date"]>split_date1)&(D["Date"]<split_date2)]
c[2]=D[D["Date"]>split_date2]


DMD = ['DK','MSZP','Zöldek']
c[1]['DK–MSZP–Dialogue']=np.where((c[1]['DK']==c[1]['MSZP']) & (c[1]['DK']==c[1]['Zöldek']),c[1]['DK'],c[1][DMD].sum(axis=1))
c[1] = c[1].drop(DMD, axis=1)




C = pd.concat(c.values(), ignore_index=True)

G=25.52
A=7.24
D=11.17
P=13.74
V=12.92
B=7.32
I=6.56
VE=3.87
O=100-G-A-D-P-V-B-I-VE
# 
# new_row = pd.DataFrame({'Date':'27 October 2024','GERB':G,'APS':A,'DPS–NN':D,'PP-DB':P,'V':V,'BSP':B,'ITN':I,'Velichie':VE,'Other':O,'DPS':np.nan}, index=[0])
# D = pd.concat([new_row,C]).reset_index(drop=True)
# D.Date=D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


C.to_csv('Hungary/poll.csv', index=False)
