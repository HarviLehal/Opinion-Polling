import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import numpy as np
import dateparser
import re

wikiurl="https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_Polish_parliamentary_election"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
df=pd.read_html(str(tables))
p = re.compile(r'\[[a-z]+\]')

# 2024 part2

data242=pd.DataFrame(df[2])
data242=data242.drop(['Polling firm/Link','Sample size','Others','Don\'t know','Lead'],axis=1)

headers = ['Date','PiS','KO','Trzecia Droga','Lewica','Razem','Konfederacja']
parties = ['PiS','KO','Trzecia Droga','Lewica','Razem','Konfederacja']
data242.columns = headers
data242.drop(data242.index[[-1]],inplace=True)
data242['Date'] = [p.sub('', x) for x in data242['Date']]
data242['Date2'] = data242['Date'].str.split('–').str[1]
data242.Date2.fillna(data242['Date'].str.split('-').str[1], inplace=True)
data242.Date2.fillna(data242.Date, inplace=True)
data242.Date = data242.Date2
data242 = data242.drop(['Date2'],axis=1)
data242.Date = data242['Date'].astype(str)
data242['Date'] = [x+' 2024' for x in data242['Date']]
data242.Date = data242.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
for z in parties:
  data242[z] = [p.sub('', x) for x in data242[z].astype(str)]
  data242[z] = pd.to_numeric(data242[z], errors='coerce')

data242 = data242.dropna(subset=['PiS'])


# 2024

data24=pd.DataFrame(df[3])
data24=data24.drop(['Polling firm/Link','Sample size','Others','Don\'t know','Lead','Nonpartisan Local Government Activists','There is One Poland'],axis=1)

headers = ['Date','PiS','KO','Trzecia Droga','Lewica','Konfederacja']
parties = ['PiS','KO','Trzecia Droga','Lewica','Konfederacja']
data24.columns = headers
data24.drop(data24.index[[-1,-2,-3,]],inplace=True)
data24=data24[data24['Date'] != '7 Apr']
data24=data24[data24['Date'] != '9 Jun	']
data24['Date'] = [p.sub('', x) for x in data24['Date']]
data24['Date2'] = data24['Date'].str.split('–').str[1]
data24.Date2.fillna(data24['Date'].str.split('-').str[1], inplace=True)
data24.Date2.fillna(data24.Date, inplace=True)
data24.Date = data24.Date2
data24 = data24.drop(['Date2'],axis=1)
data24.Date = data24['Date'].astype(str)
data24['Date'] = [x+' 2024' for x in data24['Date']]
data24.Date = data24.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
for z in parties:
  data24[z] = [p.sub('', x) for x in data24[z].astype(str)]
  data24[z] = pd.to_numeric(data24[z], errors='coerce')
data24 = data24.dropna(subset=['PiS'])


# 2023

data23=pd.DataFrame(df[4])
data23=data23.drop(['Polling firm/Link','Sample size','Others','Don\'t know','Lead','Nonpartisan Local Government Activists','There is One Poland'],axis=1)

headers = ['Date','PiS','KO','Trzecia Droga','Lewica','Konfederacja']
parties = ['PiS','KO','Trzecia Droga','Lewica','Konfederacja']
data23.columns = headers
data23.drop(data23.index[[-1,-3,]],inplace=True)
# data23['Date'] = [p.sub('', x) for x in data23['Date']]
data23['Date2'] = data23['Date'].str.split('–').str[1]
data23.Date2.fillna(data23['Date'].str.split('-').str[1], inplace=True)
data23.Date2.fillna(data23.Date, inplace=True)
data23.Date = data23.Date2
data23 = data23.drop(['Date2'],axis=1)
data23.Date = data23['Date'].astype(str)
data23['Date'] = [x+' 2023' for x in data23['Date']]
data23.Date = data23.Date.apply(lambda x: dateparser.parse(x, settings={'PREFER_DAY_OF_MONTH': 'first'}))
for z in parties:
  data23[z] = [p.sub('', x) for x in data23[z].astype(str)]
  data23[z] = pd.to_numeric(data23[z], errors='coerce')
data23 = data23.dropna(subset=['PiS'])


data = pd.concat([data242,data24,data23])
data=data[['Date','PiS','KO','Trzecia Droga','Lewica','Razem','Konfederacja']]
data.to_csv('Polish/poll.csv', index=False)



parties = ['PiS','KO','Lewica','Konfederacja', 'Trzecia Droga']
UO = ['KO', 'Lewica', 'Trzecia Droga']
R = ['PiS', 'Konfederacja']
data[parties] = data[parties].astype(float)
data['Government (KO + Lewica + Trzecia Droga)'] = data[UO].sum(axis=1)
data['Right Wing (PiS + Konfederacja)'] = data[R].sum(axis=1)
data = data.drop(UO + R, axis=1)

data.to_csv('Polish/poll2.csv', index=False)


