import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_French_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )



headers = ['1','Date','2','EXG','NFP','3','4','5','DVG','6','ENS','7','DVD','LR','8','9','RN','REC','10','DIV']
parties = ['EXG','NFP','DVG','ENS','DVD','LR','RN','REC','DIV']
drop = ['1','2','3','4','5','6','7','8','9','10']
e = {}
for i in range(1):
  e[i]=pd.DataFrame(df[i])
  e[i].columns = headers
  e[i]=e[i].drop(drop, axis=1)
  e[i]['Date2'] = e[i]['Date'].str.split('–').str[1]
  e[i].Date2.fillna(e[i].Date, inplace=True)
  e[i]['Date2'] = [x for x in e[i]['Date2'].astype(str)]
  e[i]['Date'] = e[i]['Date2']
  e[i] = e[i].drop(['Date2'], axis=1)
  e[i].Date=e[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  e[i] = e[i][e[i]['ENS'] != e[i]['DVD']]
  for z in parties: # replace any non-numeric values with NaN
    e[i][z] = [p.sub('', x) for x in e[i][z].astype(str)]
    e[i][z] = e[i][z].str.strip('%')
    e[i][z] = pd.to_numeric(e[i][z], errors='coerce')

E = pd.concat(e.values(), ignore_index=True)

E=E[E['NFP']>11]


# E['LR']=np.where(E['LR1']==E['LR1'],E['LR1'],E['LR1']+E['LR2'])

# E=E.drop(['LR1','LR2'], axis=1)








split_date = '01 Jan 2024'

split_date=dateparser.parse(split_date)

E=E[(pd.to_datetime(E["Date"]) > split_date)]

E=E[['Date','EXG','NFP','DVG','ENS','LR','DVD','RN','REC','DIV']]

new_row = pd.DataFrame({'Date':'19 June 2022','EXG':1.19,'NFP':26.16,'DVG':3.3,'ENS':25.8,'LR':11.3,'DVD':1.92,'RN':18.68,'REC':4.25,'DIV':3.8}, index=[0])
E = pd.concat([E,new_row]).reset_index(drop=True)
E.Date=E.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

E.to_csv('French/poll.csv', index=False)




