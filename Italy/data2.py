import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Italian_general_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

e = {}
for i in range(6):
  print(i)
  e[i]=pd.DataFrame(df[i+1])
  if i==0:
    headers = ['Date','FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','NM']
    parties = ['FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','NM']
    year = str(2025)
  elif i==1:
    headers = ['Date','FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','PTD','NM','ScN']
    parties = ['FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','PTD','NM','ScN']
    year = str(2024)
  elif i==2:
    headers = ['Date','FdI','PD','M5S','Lega','FI','SUE','A','AVS','PTD','DSP','Libertà','AP']
    parties = ['FdI','PD','M5S','Lega','FI','SUE','A','AVS','PTD','DSP','Libertà','AP']
    year = str(2024)
  elif i==3:
    headers = ['Date','FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','Italexit','PTD','DSP','NM']
    parties = ['FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','Italexit','PTD','DSP','NM']
    year = str(2024)
  elif i==4:
    headers = ['Date','FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','Italexit','PTD','DSP','NM']
    parties = ['FdI','PD','M5S','Lega','FI','A','IV','AVS','+E','Italexit','PTD','DSP','NM']
    year = str(2023)
  else:
    headers = ['Date','FdI','PD','M5S','Lega','FI','A-IV','AVS','+E','Italexit','PTD','DSP','NM']
    parties = ['FdI','PD','M5S','Lega','FI','A-IV','AVS','+E','Italexit','PTD','DSP','NM']
    year = str(2022)
  e[i]=e[i].drop(["Polling firm","Sample size","Others","Lead"], axis=1)
  e[i].columns = headers
  if i==1:
    e[i] = e[i][e[i]['Date'] != '9 June']
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date2'] = [x+ year for x in e[i]['Date2'].astype(str)]
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  for z in parties: # replace any non-numeric values with NaN
    e[i][z] = pd.to_numeric(e[i][z], errors='coerce')
  e[i] = e[i].dropna(subset=['FdI'])


split_date = '19 Oct 2023'

split_date=dateparser.parse(split_date)

c={}
c[0]=e[0]
c[1]=e[1]
c[2]=e[2]
c[3]=e[3]
c[4]=e[4][(pd.to_datetime(e[4]["Date"]) >= split_date)]
c[5]=e[4][(pd.to_datetime(e[4]["Date"]) < split_date)]
c[6]=e[5]

c[5]['A-IV']=np.where(c[5]['A']==c[5]['IV'],c[5]['A'],c[5]['A']+c[5]['IV'])
# c[4]['A']=np.where(c[4]['A']+c[4]['IV']>5.2,np.nan,c[4]['A'])
# c[4]['IV']=np.where(c[4]['A']==np.nan&c[4]['IV']==5.2,np.nan,c[4]['IV'])
threeway = ['A','IV']
c[5] = c[5].drop(threeway, axis=1)

C = pd.concat(c.values(), ignore_index=True)


C.to_csv('Italy/poll2.csv', index=False)


parties=['FdI', 'PD', 'M5S', 'Lega', 'FI', 'A', 'IV', 'AVS', '+E', 'PTD','NM', 'Libertà','ScN', 'SUE', 'DSP', 'AP', 'Italexit', 'A-IV']
for z in parties:
  C[z] = np.where(3>C[z],np.nan,C[z])
gov = ['FdI','Lega','FI','NM']
opp = [p for p in parties if p not in gov]

C['Government'] = C[gov].sum(axis=1)
C['Opposition'] = C[opp].sum(axis=1)
C = C.drop(gov+opp, axis=1)

C.to_csv('Italy/poll_bloc.csv', index=False)




C = pd.concat(c.values(), ignore_index=True)


gov = ['FdI','Lega','FI','NM']
opp = ['PD','M5S','AVS','+E']
for z in parties:
  C[z] = np.where(3>C[z],np.nan,C[z])
C['CDX'] = C[gov].sum(axis=1)
C['CSX'] = C[opp].sum(axis=1)
C = C.drop(gov+opp, axis=1)
C=C.dropna(axis=1, how='all')


column_to_move = C.pop("CSX")
C.insert(1, "CSX", column_to_move )

newparties = C.columns[1:]
C['total']=C[newparties].sum(axis=1)
C[newparties] = C[newparties].div(C['total'], axis=0)
C = C.drop(["total"], axis=1)



C.to_csv('Italy/poll_bloc2.csv', index=False)
