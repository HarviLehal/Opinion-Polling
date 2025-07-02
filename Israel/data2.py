import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Israeli_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

# headers = ['Date','1','2','Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Balad','3','4']
# parties = ['Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Balad']
drop = ['1','2','3','4']


d = {}
for i in range(9):
  # print(i)
  heads = []
  if i < 6:
    for j in range(len(df[i].columns)):
      heads.append(df[i].columns[j][1])
    d[i]=pd.DataFrame(df[i])
    d[i].columns = heads
    d[i]=d[i].drop(['Polling firm','Publisher','Gov. total','Opp. total'], axis=1)
    if i==2:
      d[i]=d[i].drop(['Supp. total'],axis=1)
    if i==0:
      d[i].rename(columns={'B&W':'National Unity'},inplace=True)
  else:
    for j in range(len(df[i].columns)):
      heads.append(df[i].columns[j][0])
    d[i]=pd.DataFrame(df[i])
    d[i].columns = heads
    d[i]=d[i].drop(['Polling firm','Publisher','Gov.','Opp.'], axis=1)
  # parties.remove("Others")
  # parties.replace('No Party', 'None')
  # d[i].rename(columns={'No party': 'None','Fieldwork date':'Date','Ishin':'NIK','Reiwa':'REI','Komei':'KMT'}, inplace=True)
  # d[i] = d[i].drop(d[i].columns[[1, 2,-1,-2,-4]],axis = 1)
  parties = d[i].columns[1:]
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  if i < 4:
    d[i]['Date2'] = [x+ str(2025) for x in d[i]['Date2'].astype(str)]
  elif 3 < i < 8:
    d[i]['Date2'] = [x+ str(2024) for x in d[i]['Date2'].astype(str)]
  else :
    d[i]['Date2'] = [x+ str(2023) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i].dropna(subset=['Date'])
  for z in parties:
    d[i][z] = [p.sub('', x) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('%','') for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('(','') for x in d[i][z].astype(str)]
    d[i][z] = [x.replace(')','') for x in d[i][z].astype(str)]
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
  d[i] = d[i].dropna(subset=['Likud'])
  if min(d[i]['Date']) < dateparser.parse('28 May 2024') < max(d[i]['Date']):
    # print('fix time')
    # if d[i]['Date']) > dateparser.parse('29 May 2024'):
    #   d[i]['Democrats']=np.where(d[i]['Labor']+d[i]['Meretz']>12,d[i]['Labor'],d[i]['Labor']+d[i]['Meretz'])
    #   d[i]['Labor']=np.nan
    #   d[i]['Meretz']=np.nan
    # if greater than dateparser.parse('29 May 2024'), then we want to define Democrats as the sum of Labor and Meretz, unless Labor and Meretz sum is greater than 12, in which case we want to define Democrats as Labor in the subset of d[i] where Date is greater than dateparser.parse('29 May 2024')
    for rows in d[i].index:
      if d[i].loc[rows,'Date'] > dateparser.parse('28 May 2024'):
        d[i].loc[rows,'Democrats'] = d[i].loc[rows,'Labor'] + d[i].loc[rows,'Meretz']
        if d[i].loc[rows,'Democrats'] > 12:
          d[i].loc[rows,'Democrats'] = d[i].loc[rows,'Labor']
        d[i].loc[rows,'Labor'] = np.nan
        d[i].loc[rows,'Meretz'] = np.nan
      else:
        d[i].loc[rows,'Democrats'] = np.nan
D = pd.concat(d.values(), ignore_index=True)

D.loc[len(D.index)-1,['Date']] = '2022-11-01'
D.loc[len(D.index)-2,['Date']] = '2022-12-23'
D.Date = D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

parties = D.columns[1:]

D[parties] = D[parties].astype(float)
fascist = ['Mafdal– RZ','Otzma Yehudit','Noam']
D['RZP-OY-Noam']=np.where(D['Mafdal– RZ']==D['Noam'], D['Mafdal– RZ'], D[fascist].sum(axis=1))
D = D.drop(fascist, axis=1)
parties = parties.drop(fascist)

# print(D)

D=D[['Date','Likud','Yesh Atid','RZP-OY-Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu',"Ra'am","Hadash –Ta'al",'Labor','Meretz','Democrats','Balad','Bennett 2026']]

D.to_csv('Israel/poll.csv', index=False)

