import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Israeli_legislative_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))

headers = ['Date','1','2','Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Balad','3','4']
parties = ['Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Balad']
drop = ['1','2','3','4']

d = {}
for i in range(4):
  print(i)
  if i == 0:
    headers = ['Date','1','2','Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Democrats','Balad','3','4']
    parties = ['Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Democrats','Balad']
  elif i == 1:
    headers = ['Date','1','2','Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Balad','3','4']
    parties = ['Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Balad']
  else:
    headers = ['Date','1','2','Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Balad','3','4']
    parties = ['Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Balad']
    drop = ['1','2','3','4']
  d[i]=pd.DataFrame(df[i])
  d[i].columns = headers
  d[i]=d[i].drop(drop, axis=1)
  d[i]['Date2'] = d[i]['Date'].str.split('–').str[1]
  d[i].Date2.fillna(d[i].Date, inplace=True)
  if i == 0:
    d[i]['Date2'] = [x+ str(2024) for x in d[i]['Date2'].astype(str)]
  if i == 1:
    d[i]['Date2'] = [x+ str(2024) for x in d[i]['Date2'].astype(str)]
  if i == 2:
    d[i]['Date2'] = [x+ str(2024) for x in d[i]['Date2'].astype(str)]
  if i == 3:
    d[i]['Date2'] = [x+ str(2023) for x in d[i]['Date2'].astype(str)]
  d[i]['Date'] = d[i]['Date2']
  d[i] = d[i].drop(['Date2'], axis=1)
  d[i].Date=d[i].Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
  d[i] = d[i][d[i]['Likud'] != d[i]['Otzma Yehudit']]
  for z in parties:
    d[i][z] = [x.replace('–',str(np.NaN)) for x in d[i][z].astype(str)]
    d[i][z] = [x.replace('—',str(np.NaN)) for x in d[i][z].astype(str)]
  if i ==0:
    d[i].drop(d[i].index[[-1]],inplace=True)
  if i ==1:
    d[i].drop(d[i].index[[-1]],inplace=True)
  if i ==3:
    d[i].drop(d[i].index[[-1]],inplace=True)
  if i ==3:
    d[i].drop(d[i].index[[-2]],inplace=True)
  for z in parties: # replace any non-numeric values with NaN
    d[i][z] = pd.to_numeric(d[i][z], errors='coerce')
    
    
split_date = '29 May 2024'

split_date=dateparser.parse(split_date)

c={}
c[0]=d[0]
c[1]=d[1][(pd.to_datetime(d[1]["Date"]) > split_date)]
c[2]=d[1][(pd.to_datetime(d[1]["Date"]) < split_date)]
c[3]=d[2]
c[4]=d[3]

c[1]['Democrats']=np.where(c[1]['Labor']+c[1]['Meretz']>12,c[1]['Labor'],c[1]['Labor']+c[1]['Meretz'])
threeway = ['Labor','Meretz']
c[1] = c[1].drop(threeway, axis=1)


D = pd.concat(c.values(), ignore_index=True)
D.loc[len(D.index)-1,['Date']] = '2022-11-01'
D.Date = D.Date.astype(str).apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))


parties = ['Likud','Yesh Atid','Mafdal-RZ','Otzma Yehudit','Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Democrats','Balad']

D[parties] = D[parties].astype(float)
fascist = ['Mafdal-RZ','Otzma Yehudit','Noam']
D['RZP-OY-Noam']=np.where(D['Mafdal-RZ']==D['Noam'], D['Mafdal-RZ'], D[fascist].sum(axis=1))
D = D.drop(fascist, axis=1)

print(D)

D=D[['Date','Likud','Yesh Atid','RZP-OY-Noam','National Unity','New Hope','Shas','UTJ','Yisrael Beiteinu','Raam','Hadash-Taal','Labor','Meretz','Democrats','Balad']]

D.to_csv('Israel/poll.csv', index=False)

