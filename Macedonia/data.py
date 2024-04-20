import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import dateparser
import re
import numpy as np

wikiurl="https://en.wikipedia.org/wiki/2024_North_Macedonian_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

data=pd.DataFrame(df[-2])
headers = ['drop1','Date','drop2','SDSM','LDP','Besa','LD','A','drop5','ASh','BDI','drop3','VMRO-DPMNE','Levica','ZNAM','Other','drop4']
parties = ['SDSM','LDP','Besa','LD','A','ASh','BDI','VMRO-DPMNE','Levica','ZNAM','Other']
drops = ['drop1','drop2','drop3','drop4','drop5']

data.columns = headers
data=data.drop(drops, axis=1)
data = data[data['Date'] != '17 Oct 2021']
data = data[data['Date'] != 'Mar 2023']

for z in parties:
  data[z] = [p.sub('', x) for x in data[z].astype(str)]
  data[z] = [x.replace('-',str(np.NaN)) for x in data[z]]
  data[z] = [x.replace('—',str(np.NaN)) for x in data[z]]
  data[z] = [x.replace('–',str(np.NaN)) for x in data[z]]
  data[z] = data[z].astype('float')


data['Date'] = [p.sub('', x) for x in data['Date'].astype(str)]
data['Date2'] = data['Date'].str.split('–').str[1]
data.Date2.fillna(data['Date'].str.split('-').str[1], inplace=True)
data.Date2.fillna(data.Date, inplace=True)
data.Date = data.Date2
data = data.drop(['Date2'],axis=1)
data.Date = data['Date'].astype(str)
data.Date = data.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

SDSM=['SDSM','LDP']
VLEN=['Besa','LD','A']
EF=['ASh','BDI']

data['LDP']=np.where(data['SDSM']==data['LDP'],np.NaN,data['LDP'])
data['Besa']=np.where(data['SDSM']==data['Besa'],np.NaN,data['Besa'])
data['A']=np.where(data['A']==data['ASh'],np.NaN,data['A'])
data['VLEN']=np.where(data['LD']==data['Besa'],data['Besa'],data[VLEN].sum(axis=1))
data['VLEN']=np.where(data['VLEN']==0,np.NaN,data['VLEN'])
data['European Front']=data[EF].sum(axis=1)
data['European Future']=data[SDSM].sum(axis=1)
data = data.drop(VLEN+EF+SDSM, axis=1)

data=data[['Date','European Future','VMRO-DPMNE','European Front','Levica','VLEN','ZNAM','Other']]
headers=['Date','SDSM','VMRO-DPMNE','BDI','Levica','VLEN','ZNAM','Other']
data.columns = headers

data.to_csv('Macedonia/poll.csv', index=False)

