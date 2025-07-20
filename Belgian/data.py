import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_les_%C3%A9lections_belges_de_2029"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables), decimal=',', thousands='.')
p = re.compile(r'\[[^\]]*\]')

# VLAANDEREN

data=pd.DataFrame(df[2])
headers = ['Date','1','2','3','N-VA','VB','Vooruit','CD&V','Open Vld','PVDA','Groen','Overig','4']
parties = ['N-VA','VB','Vooruit','CD&V','Open Vld','PVDA','Groen','Overig']
drop = ['1','2','3','4']
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
  data[z] = data[z].astype(str)
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace('-',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace('NC',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace(',', '.') for x in data[z].astype(str)]
  data[z] = data[z].astype(str)
  data[z] = data[z].str.strip('%')
  data[z] = data[z].astype('float')
data=data.dropna(subset=['VB'])

data.drop(data.index[[-1]],inplace=True)

data.to_csv('Belgian/poll_vlaanderen.csv', index=False)


# WALLONIE

data=pd.DataFrame(df[0])
headers = ['Date','1','2','3','MR','PS','LE','PTB','Ecolo','DéFI','Autres','4']
parties = ['PS','MR','Ecolo','PTB','LE','DéFI','Autres']
drop = ['1','2','3','4']
data.columns = headers
data=data.drop(drop, axis=1)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data = data[data['MR'] != data['Ecolo']]
for z in parties:
  data[z] = data[z].astype(str)
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace('-',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace('NC',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace(',', '.') for x in data[z].astype(str)]
  data[z] = data[z].astype(str)
  data[z] = data[z].str.strip('%')
  data[z] = data[z].astype('float')
data=data.dropna(subset=['PS'])

data.drop(data.index[[-1]],inplace=True)

data.to_csv('Belgian/poll_wallonie.csv', index=False)


# BRUSSEL

data=pd.DataFrame(df[1])
headers = ['Date','1','2','3','Ecolo','MR','PS','PVDA-PTB','DéFI','LE','N-VA','Open vld','VB','CD&V','Groen','Vooruit','drop4','drop5','drop6','drop7']
parties = ['Ecolo','PS','MR','PVDA-PTB','DéFI','LE','N-VA','Open vld','VB','CD&V','Groen','Vooruit']

headers = ['Date','1','2','3','MR','PS','PTB','Ecolo','LE','DéFI','Groen','TFA','N-VA','Open vld','VB','Vooruit','PVDA','CD&V','Autres','4']
parties = ['MR','PS','PTB','Ecolo','LE','DéFI','Groen','TFA','N-VA','Open vld','VB','Vooruit','PVDA','CD&V','Autres']

drop = ['1','2','3','4']
data.columns = headers
data=data.drop(drop, axis=1)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data = data[data['MR'] != data['Ecolo']]
for z in parties:
  data[z] = data[z].astype(str)
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace('-',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace('NC',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace(',', '.') for x in data[z].astype(str)]
  data[z] = data[z].astype(str)
  data[z] = data[z].str.strip('%')
  data[z] = data[z].astype('float')
data=data.dropna(subset=['PS'])

data.drop(data.index[[-1]],inplace=True)

left = ['PVDA','PTB']
data['PTB-PVDA'] = data[left].sum(axis=1)
socialist = ['PS','Vooruit']
data['PS-Vooruit'] = data[socialist].sum(axis=1)
green = ['Groen','Ecolo']
data['Ecolo-Groen'] = data[green].sum(axis=1)
liberal = ['MR','Open vld']
data['MR-Open vld'] = data[liberal].sum(axis=1)
jesus = ['CD&V','LE']
data['LE-CD&V'] = data[jesus].sum(axis=1)
data = data.drop(left+socialist+green+liberal+jesus,axis=1)

data = data[['Date','MR-Open vld','PS-Vooruit','PTB-PVDA','Ecolo-Groen','LE-CD&V','DéFI','TFA','N-VA','VB','Autres']]

data.to_csv('Belgian/poll_brussel.csv', index=False)


# SEATS BY PARTY

data=pd.DataFrame(df[3])
headers = ['Date','1','2','N-VA','VB','MR','PS','PVDA-PTB','LE','Vooruit','CD&V','Open vld','Groen','Ecolo','DéFI','Others','3','Government','Opposition','4']
parties = ['N-VA','VB','MR','PS','PVDA-PTB','LE','Vooruit','CD&V','Open vld','Groen','Ecolo','DéFI','Others','Government','Opposition']
drop = ['1','2','3','4']
data.columns = headers
data=data.drop(drop, axis=1)
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
data = data[data['DéFI'] != data['MR']]
for z in parties:
  data[z] = data[z].astype(str)
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('–',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace('-',str(np.nan)) for x in data[z].astype(str)]
  data[z] = [x.replace('NC',str(np.nan)) for x in data[z].astype(str)]
  data[z] = data[z].astype(str)
  data[z] = data[z].astype('float')

print(data)

bloc = ['Government','Opposition']
data1 = data.drop(bloc, axis=1)
data1=data1.dropna(subset=['VB'])
data1.to_csv('Belgian/seats.csv', index=False)
parties = ['N-VA','VB','MR','PS','PVDA-PTB','LE','Vooruit','CD&V','Open vld','Groen','Ecolo','DéFI','Others']
data2 = data.drop(parties, axis=1)
data2=data2.dropna(subset=['Government'])
data2.to_csv('Belgian/seats2.csv', index=False)



# left = ['PVDA-PTB']
# green = ['Ecolo','Groen']
# socialist = ['PS','Vooruit']
# liberal = ['MR','Open vld','LE','DéFI']
# christian = ['CD&V']
# flemish = ['N-VA']
# right = ['VB']
# 
# data[parties] = data[parties].astype(float)
# data['left (PVDA-PTB)'] = data[left].sum(axis=1)
# data['green (Ecolo,Groen)'] = data[green].sum(axis=1)
# data['socialist (PS,Vooruit)'] = data[socialist].sum(axis=1)
# data['liberal (MR,Open vld,LE,DéFI)'] = data[liberal].sum(axis=1)
# data['christian (CD&V)'] = data[christian].sum(axis=1)
# data['flemish (N-VA)'] = data[flemish].sum(axis=1)
# data['far right (VB)'] = data[right].sum(axis=1)
# data = data.drop(parties, axis=1)
# data.to_csv('Belgian/seats_coalition.csv', index=False)

