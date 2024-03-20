import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_Belgian_elections"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]'  )

# VLAANDEREN

data=pd.DataFrame(df[0])
headers = ['Date','drop1','drop2','drop3','N-VA','VB','CD&V','Open Vld','Vooruit','Groen','PVDA','drop4','drop5','drop6','drop7','drop8']
parties = ['N-VA','VB','CD&V','Open Vld','Vooruit','Groen','PVDA']
drop = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7','drop8']
data.columns = headers
data=data.drop(drop, axis=1)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data = data[data['VB'] != data['Groen']]
for z in parties:
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z].astype(str)]
  data[z] = data[z].astype(str)
  data[z] = data[z].str.strip('%')
  data[z] = data[z].astype('float')
  
print(data)

data.to_csv('Belgian/poll_vlaanderen.csv', index=False)


# WALLONIE

data=pd.DataFrame(df[3])
headers = ['Date','drop1','drop2','drop3','PS','MR','Ecolo','PTB','LE','DéFI','drop4','drop5','drop6','drop7']
parties = ['PS','MR','Ecolo','PTB','LE','DéFI']
drop = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7']
data.columns = headers
data=data.drop(drop, axis=1)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data = data[data['DéFI'] != data['PS']]
for z in parties:
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z].astype(str)]
  data[z] = data[z].astype(str)
  data[z] = data[z].str.strip('%')
  data[z] = data[z].astype('float')
  
print(data)

data.to_csv('Belgian/poll_wallonie.csv', index=False)


# BRUSSEL

data=pd.DataFrame(df[5])
headers = ['Date','drop1','drop2','drop3','Ecolo','PS','MR','PVDA-PTB','DéFI','LE','N-VA','Open vld','VB','cd&v','Groen','Vooruit','drop4','drop5','drop6','drop7']
parties = ['Ecolo','PS','MR','PVDA-PTB','DéFI','LE','N-VA','Open vld','VB','cd&v','Groen','Vooruit']
drop = ['drop1','drop2','drop3','drop4','drop5','drop6','drop7']
data.columns = headers
data=data.drop(drop, axis=1)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data = data[data['Vooruit'] != data['PS']]
for z in parties:
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z].astype(str)]
  data[z] = data[z].astype(str)
  data[z] = data[z].str.strip('%')
  data[z] = data[z].replace(r'^([A-Za-z]|[0-9]|_)+$', np.NaN, regex=True)
  data[z] = data[z].astype('float')

print(data)

data.to_csv('Belgian/poll_brussel.csv', index=False)


# SEATS BY PARTY

data=pd.DataFrame(df[6])
headers = ['Date','drop1','drop2','N-VA','PS','VB','MR','Ecolo','cd&v','Open vld','PVDA-PTB','Vooruit','Groen','LE','DéFI','drop4','drop5','drop6','drop7','drop8']
parties = ['N-VA','PS','VB','MR','Ecolo','cd&v','Open vld','PVDA-PTB','Vooruit','Groen','LE','DéFI']
drop = ['drop1','drop2','drop4','drop5','drop6','drop7','drop8']
data.columns = headers
data=data.drop(drop, axis=1)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data = data[data['DéFI'] != data['PS']]
for z in parties:
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z].astype(str)]
  data[z] = data[z].astype(str)
  data[z] = data[z].astype('float')

print(data)

data.to_csv('Belgian/seats.csv', index=False)

left = ['PVDA-PTB']
green = ['Ecolo','Groen']
socialist = ['PS','Vooruit']
liberal = ['MR','Open vld','LE','DéFI']
christian = ['cd&v']
flemish = ['N-VA']
right = ['VB']

data[parties] = data[parties].astype(float)
data['left (PVDA-PTB)'] = data[left].sum(axis=1)
data['green (Ecolo,Groen)'] = data[green].sum(axis=1)
data['socialist (PS,Vooruit)'] = data[socialist].sum(axis=1)
data['liberal (MR,Open vld,LE,DéFI)'] = data[liberal].sum(axis=1)
data['christian (cd&v)'] = data[christian].sum(axis=1)
data['flemish (N-VA)'] = data[flemish].sum(axis=1)
data['far right (VB)'] = data[right].sum(axis=1)
data = data.drop(parties, axis=1)
data.to_csv('Belgian/seats_coalition.csv', index=False)

