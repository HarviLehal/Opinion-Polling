import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re


wikiurl="https://en.wikipedia.org/wiki/2023_Montenegrin_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

data22=pd.DataFrame(df[1])
data22 = data22.drop(['Polling firm/source','Others','Lead','SNP','UCG','Prava','DP','Demos','LSh','KSh'],axis=1)
headers = ['Date','DPS','SD','DF','DCG','CnB','BS','SDP','PES']
parties = ['DPS','SD','DF','DCG','CnB','BS','SDP','PES']
data22.columns = headers


data22['Date2'] = data22['Date'].str.split('–').str[1]
data22.Date2.fillna(data22['Date'].str.split('-').str[1], inplace=True)
data22.Date2.fillna(data22.Date, inplace=True)
data22.Date = data22.Date2
data22 = data22.drop(['Date2'],axis=1)
data22.Date = data22['Date'].astype(str)
data22.Date = data22.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))

for z in parties:
  data22[z] = [p.sub('', x) for x in data22[z].astype(str)]
  data22[z] = [x.replace('–',str(np.nan)) for x in data22[z]]
  data22[z] = data22[z].astype('float').astype(str)

data22.to_csv('Montenegro/poll.csv', index=False)
